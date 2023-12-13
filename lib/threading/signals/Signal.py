from abc import ABC, abstractclassmethod

class Signal(ABC):
  def __init__(self, task_id) -> None:
    super().__init__()
    self.task_id = task_id

  @abstractclassmethod
  def __str__(self) -> str:
    pass