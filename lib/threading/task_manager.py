import threading
from .signals.Signal import Signal
from .task import Task

class TaskManager:
    def __init__(self):
        self.threads = []
        self.signals = {
            0: []
        }
        pass

    def __get_task_id__(task_index: int):
        return f"T_{task_index}"

    def __get_thread_id__(task_id: str):
        chunks = task_id.split('_')
        return int(chunks[1])

    def start(self, task: Task):
        self.is_running = True
        task_id = TaskManager.__get_task_id__(len(self.threads))
        thread = threading.Thread(target=self.task_runner, args=(task, task_id,))
        self.threads.append(thread)
        self.signals[task_id] = []
        thread.start()
        return task_id

    def task_runner(self, task: Task, task_id: str):
        execution_context = task.execute()
        for i in execution_context:
            if(len(self.signals[task_id]) == 0): continue
            
            while (len(self.signals[task_id]) > 0):
                signal: Signal = self.signals[task_id].pop()
                execution_context.send(str(signal))

    def stop(self):
        self.is_running = False
    
    def emit_signal(self, sign: Signal):
        self.signals[sign.task_id].append(sign)
        pass
