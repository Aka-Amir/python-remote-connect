
class DataParser:
  def DecodeData(data):
    chunks = str(data.decode()).split(';')
    data_dict = {}
  
    for item in chunks:
      chunk = item.split('=')
      data_dict[chunk[0]] = chunk[1]
    
    return data_dict
  
  def EncodeData(data: dict):
    encoded_data = ""
    for key in list(data.keys()):
      encoded_data = encoded_data + f"{key}={data[key]};"
    return encoded_data.encode()