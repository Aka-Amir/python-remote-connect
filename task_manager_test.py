import time

from lib.threading.task import Task
from lib.threading.signals import signals
from lib.threading.task_manager import TaskManager

taskManager = TaskManager()

def Count(start_at: int, ends_at: int):
  for i in range(start_at, ends_at):
    print(i)
    time.sleep(1)
    yield None



task_one = Task(Count, 0, 10)
task_two = Task(Count, 0, 10)

task_1 = taskManager.start(task_one)
task_2 = taskManager.start(task_two)


while (not task_one.stop):
  taskManager.emit_signal(signals.ContinueSignal(task_1))
  taskManager.emit_signal(signals.PauseSignal(task_2))
  time.sleep(3)
  taskManager.emit_signal(signals.ContinueSignal(task_2))
  taskManager.emit_signal(signals.PauseSignal(task_1))
  time.sleep(1)

