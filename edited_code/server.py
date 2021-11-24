import pickle, hmac, hashlib, json
from typing import Union

def reverse_fun() -> Union[str, dict]:
      with open("users.json","rb") as f:
            data = f.read()
            json_data: dict = json.loads(data)
      if hmac.new(b'shared-public-key', pickle.dumps({"username":json_data["username"],"password":json_data["password"]}), hashlib.sha1).hexdigest() == json_data["signature"]:
            return json_data
      else:
            return 'Integrity Error'
      

if __name__ == '__main__':
      print(reverse_fun())