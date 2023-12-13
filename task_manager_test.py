import time

from lib.threading.task import Task
from lib.threading.task_manager import TaskManager
from lib.threading.signals import kill_sign

taskManager = TaskManager()

def Count(start_at: int, ends_at: int):
  for i in range(start_at, ends_at):
    print(i)
    time.sleep(1)
    yield None



count_task = Task(Count, 0, 10)

t_id = taskManager.start(count_task)

time.sleep(3)
taskManager.emit_signal(kill_sign.KillSignal(t_id))

