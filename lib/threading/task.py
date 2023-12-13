import inspect

class Task():

  def __init__(self, fn , *args) -> None:
    if not inspect.isgeneratorfunction(fn):
      raise TypeError('Generator function required')
    self.params = tuple(args)
    print(self.params)
    self.__fn__ = fn
    self.stop = False
    
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
    yield 'EXIT_0'

  def __process_signal__(self, signal: str):
    if (signal.startswith('SIGKILL')):
      self.stop = True
    
