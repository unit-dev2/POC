from flask import request
from flask_restful import Resource, abort
from threading import Thread
from actions import actions
from action_logs import action_logs
from api.core.action import ActionCore
from api.core.notify.slack import SlackNotifyCore


class ActionList(Resource):
    
    def get(self):
        return { "results": actions }
    
    def post(self):
        Action_Core = ActionCore()
        Slack_Notify_Core = SlackNotifyCore()
        data = request.json
        print("actions[-1]: ", actions[-1])
        last_action_id = actions[-1].get("id")
        all_targets_non_execute_actions = all(target for target in data["targets"] if Action_Core.find_by_ip(target) is None)
        print("all_targets_non_execute_actions: ", all_targets_non_execute_actions)
        if all_targets_non_execute_actions:
            new_action = { "id": last_action_id + 1, **data, "status": "in progress" }
            actions.append(new_action)
            print("****************** Hasta aca llega ******************")
            thread = Thread(target=Action_Core.execute_ping_multi, kwargs={"action_id": new_action.get("id")})
            thread.start()
            ##Slack_Notify_Core.send_notification(new_action)
            Slack_Notify_Core.send_notification_with_notify(new_action)
            return { "msg": "Action created", "action": new_action }
        else:
            abort(500)


class ActionResource(Resource):
    
    def get(self, action_id):
        actionFound = next(filter(lambda action: action.get("id") == action_id, actions), None)

        if actionFound is None:
            abort(404)

        return { "action": actionFound }
    

class ActionLogResource(Resource):
    
    def get(self, action_id):
        logs_found = list(filter(lambda log: log.get("action_id") == action_id, action_logs))
        return { "action logs": logs_found }
