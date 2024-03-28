import os

class SlackNotifyCore:

    def __init__(self) -> None:
        pass


    def _convert_json_to_string(self, action):
        action_arguments = action.get("arguments", {})
        return f"""
        ACTION CREATED
        ------------------------
        action id: {action.get("id", None)}
        command: {action.get("command", None)}
        targets: {action.get("targets", [])}
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
        targets: {action.get("targets", None)}
        status: {action.get("status", None)}
        """


    def send_notification_with_notify(self, json_data):
        action_string = self._convert_json_to_string(json_data)
        os.system(f"echo '{action_string}' | notify -bulk")


    def send_notification_on_update_with_notify(self, action):
        action_string = self._convert_json_to_update_string(action)
        os.system(f"echo '{action_string}' | notify -bulk")
