from flask import request
from flask_restful import Resource, abort
from threading import Thread
from actions import actions
from action_logs import action_logs
from api.core.action import ActionCore


class ActionList(Resource):
    
    def get(self):
        return { "results": actions }
    
    def post(self):
        Action_Core = ActionCore()
        data = request.json
        last_action_id = actions[-1].get("id")
        if Action_Core.find_by_ip(data["target"]) is None:
            new_action = { "id": last_action_id + 1, **data, "status": "in progress" }
            actions.append(new_action)
            thread = Thread(target=Action_Core.execute_ping, kwargs={"action_id": new_action.get("id")})
            thread.start()
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
