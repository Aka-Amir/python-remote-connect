class PayloadModel:
  command = ''
  data = ''
  __build_pipe_line__ = []
  
  def __init__(self, command: str = '', payload = '', as_dict: dict = { 'command': '', 'data': '' }) -> None:
    self.command = command
    self.data = payload

    if self.command == '' : self.command = as_dict['command']
    if self.data == '': self.data = as_dict['data']

    pass


  def set_command(self, command):
    self.command = command
    return self
  
  def set_payload(self, payload):
    self.data = payload
    return self

  def pipe(self, *args: list):
    for pipe_line in args:
      self.__build_pipe_line__.append(pipe_line)
    return self

  def build(self):
    result = {
      'command': self.command,
      'data': self.data 
    }

    for pipe_line in self.__build_pipe_line__:
      result = pipe_line(result)

    return result