from lib.server import EventBaseServer


class Application:
  def __init__(self, server: EventBaseServer ) -> None:
    self.server = server
    server.subscribe('click', self.click)
    server.run()

  def click():
    print('Click event has fired')
    pass

if(__name__ == '__main__'):
  Application(EventBaseServer('0.0.0.0', 3500))