import inspect

class Task():

  def __init__(self, fn , *args) -> None:
    if not inspect.isgeneratorfunction(fn):
      raise TypeError('Generator function required')
    self.params = tuple(args)
    print(self.params)
    self.__fn__ = fn
    self.stop = False
    self.pause = False
    pass

  def execute(self):
    generation = self.__fn__(*self.params)
    for i in generation:
      signals = yield
      if not signals == None:
        self.__process_signal__(signals)
      
      if(self.stop):
        yield 'EXIT_1'
        break
      yield i
    self.stop = True
    yield 'EXIT_0'

  def __process_signal__(self, signal: str):
    if (signal.startswith('SIGKILL')):
      self.stop = True
    if (signal.startswith('SIGPAUSE')):
      self.pause = True
    if(signal.startswith('SIGCONT')):
      self.pause = False
    
