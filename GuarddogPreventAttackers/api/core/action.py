import math
import subprocess
import progressbar
import time
from actions import actions
from action_logs import action_logs

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
        for i, a in enumerate(actions):
            if a.get("id") == action_id:
                actions[i] = {**a, "status": "completed"}
                action = actions[i]

        if action is None:
            print("---- Error on update action with ID: ", action_id)

    
    def _add_action_log(self, action_id, action_messages):
        last_action_log_id = action_logs[-1].get("id")
        new_action_log = { "id": last_action_log_id + 1, "action_id": action_id, "action_messages": action_messages }
        action_logs.append(new_action_log)


    def find_by_ip(self, target):
        print("target: ", target)
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
        print("target: ", target)
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
