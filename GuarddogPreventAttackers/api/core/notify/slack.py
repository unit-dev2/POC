import os
import requests

class SlackNotifyCore:

    def __init__(self) -> None:
        self._webhook_url = "https://hooks.slack.com/services/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"
        self._headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}


    def _convert_json_to_string(self, action):
        action_arguments = action.get("arguments", {})
        return f"""
        ACTION CREATED
        ------------------------
        action id: {action.get("id", None)}
        command: {action.get("command", None)}
        target: {action.get("target", None)}
        arguments:
          - frequency: {action_arguments.get("frequency", None)}
          - quantity: {action_arguments.get("quantity", None)}
          - duration: {action_arguments.get("duration", None)}
        status: {action.get("status", None)}
        """
    

    def _convert_json_to_update_string(self, action):
        return f"""
        ACTION UPDATED
        ------------------------
        action id: {action.get("id", None)}
        command: {action.get("command", None)}
        target: {action.get("target", None)}
        status: {action.get("status", None)}
        """


    def send_notification(self, json_data):
        action_string = self._convert_json_to_string(json_data)
        payload = "{ 'text': " + action_string + "}"
        print("payloead: ", payload)
        response = requests.post(self._webhook_url, data=payload, headers=self._headers)
        print("response: ", response)


    def send_notification_with_notify(self, json_data):
        action_string = self._convert_json_to_string(json_data)
        os.system(f"echo '{action_string}' | notify -bulk")


    def send_notification_on_update_with_notify(self, action):
        action_string = self._convert_json_to_update_string(action)
        os.system(f"echo '{action_string}' | notify -bulk")
