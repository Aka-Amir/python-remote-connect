
from .Signal import Signal

class PauseSignal(Signal):
  def __init__(self, task_id) -> None:
    super().__init__(task_id)

  def __str__(self) -> str:
    return "SIGPAUSE"