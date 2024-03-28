import math
import subprocess
import progressbar
import time
import sys
from threading import Thread
from actions import actions
from action_logs import action_logs
from .notify.slack import SlackNotifyCore

class ActionCore:

    def _get_progress_duration(self, arguments) -> tuple[int, int]:
        progress_duration = 0
        progress_frequency = 0
        frequency = arguments.get("frequency", None)
        quantity = arguments.get("quantity", None)
        duration = arguments.get("duration", None)
        
        if frequency and quantity:
            progress_frequency = frequency
            progress_duration = (frequency * (quantity - 1)) + 2
        
        elif frequency and duration:
            progress_frequency = frequency
            progress_duration = duration + 2
        
        elif quantity and duration:
            progress_duration = duration

            if duration % quantity == 0:
                progress_frequency = round(duration / quantity)

            else:
                progress_duration = duration + 1
                progress_frequency = math.ceil(duration / quantity)
        
        return progress_duration, progress_frequency

    
    def _update_action(self, action_id):
        action = None
        Slack_Notify_Core = SlackNotifyCore()
        for i, a in enumerate(actions):
            if a.get("id") == action_id:
                actions[i] = {**a, "status": "completed"}
                action = actions[i]
                #Slack_Notify_Core.send_notification_on_update_with_notify(action)

        if action is None:
            print("---- Error on update action with ID: ", action_id)

    
    def _add_action_log(self, action_id, action_messages):
        last_action_log_id = action_logs[-1].get("id")
        new_action_log = { "id": last_action_log_id + 1, "action_id": action_id, "action_messages": action_messages }
        action_logs.append(new_action_log)


    def find_by_ip(self, target):
        action = None
        for i, a in enumerate(actions):
            if a.get("target") == target and a.get("status") == "in progress":
                action = a

        return action


    def execute_ping(self, action_id):
        action_messages = []
        action = actions[action_id - 1]
        arguments = action.get("arguments")
        target = action.get("target")
        #print("target: ", targets)
        progress_duration, progress_frequency = self._get_progress_duration(arguments)

        command = ["ping", "-w", "1", f"{target}"]

        start_time = time.time()

        with progressbar.ProgressBar(max_value=progress_duration) as bar:
            
            for i in range(progress_duration):
                #print("time = ", math.floor(time.time() - start_time))
                bar.update(i)
                if (math.floor(time.time() - start_time) % progress_frequency) == 0:
                    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = process.communicate()
                    action_messages.append(stdout.decode())
                    #print(f"Elapsed time: {time.time() - start_time}")
                
                else:
                    time.sleep(1)

        end_time = time.time()
        elapsed_time = math.floor(end_time - start_time)
        print(f'Total Time elapsed : {elapsed_time} seconds')
        print("")
        self._update_action(action_id)
        self._add_action_log(action_id, action_messages)


    def _update_action_bars(self, action_details, index):
        for action in action_details:
            action["bar"].update(index)


    def execute_action(self, action):
        target = action["target"]
        command = ["ping", "-w", "1", f"{target}"]
        #print("command: ", command)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()


    def execute_tread(self, thread):
        thread.start()


    def wait_tread(self, thread):
        thread.join()


    def execute_ping_multi(self, action_id):
        print("----------------- Aca entraaaaaa -----------------")
        action_messages = []
        action = actions[action_id - 1]
        arguments = action.get("arguments")
        targets = action.get("targets")
        print("target: ", targets)
        progress_duration, progress_frequency = self._get_progress_duration(arguments)

        start_time = time.time()

        #bars = [
        #    progressbar.ProgressBar(
        #        max_value=progress_duration,
        #        line_offset=i + 1,
        #        max_error=False
        #    ) for i in range(len(targets))
        #]

        action_details = [
            {
                "bar": progressbar.ProgressBar(
                    max_value=progress_duration,
                    line_offset=i + 1,
                    max_error=False),
                "target": target
            } for i, target in enumerate(targets)
        ]

        print_fd = progressbar.LineOffsetStreamWrapper(lines=0, stream=sys.stdout)
        assert print_fd

        for i in range(progress_duration):
            #print("time = ", math.floor(time.time() - start_time))
            #bar.update(i)            
            self._update_action_bars(action_details, i)

            if (math.floor(time.time() - start_time) % progress_frequency) == 0:
                actions_thread = [ Thread(target=self.execute_action, kwargs={"action": action}) for action in action_details ]
                #print("test 1")
                #print("test 2")
                list(map(self.execute_tread, actions_thread))
                
                #print("test 3")
                list(map(self.wait_tread, actions_thread))
                #print("test 4")
                #action_messages.append(stdout.decode())
                #print(f"Elapsed time: {time.time() - start_time}")
            
            else:
                time.sleep(1)

            #thread = Thread(target=Action_Core.execute_ping, kwargs={"action_id": new_action.get("id")})
            #thread.start()

        # Cleanup the bars
        for action in action_details:
            action["bar"].finish()
            # Add a newline to make sure the next print starts on a new line
            #print()
