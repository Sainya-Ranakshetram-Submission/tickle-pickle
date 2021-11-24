import json, pickle, hashlib, hmac

def fun(name: str,password: str) -> None:
    s = {"username":name,"password":hashlib.md5(password.encode()).hexdigest()}
    with open("users.json","w") as f:
        signature = hmac.new(b'shared-public-key', pickle.dumps(s), hashlib.sha1).hexdigest()
        s.update({'signature': signature})
        f.write(json.dumps(s))

if __name__ == '__main__':
    u = input("Username : ")
    p = input("Password : ")
    fun(u,p)