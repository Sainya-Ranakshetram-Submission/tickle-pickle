# Tickle Pickle
Submission for the tickle pickle challenge

Here we were given two different files [client.py](https://github.com/Sainya-Ranakshetram-Submission/tickle-pickle/blob/master/default_unedited_code/client.py) and [server.py](https://github.com/Sainya-Ranakshetram-Submission/tickle-pickle/blob/master/default_unedited_code/server.py)
and here is the problem statement,
```
- Find out what the vulnerability is.
- Create a exploit code so that you can exploit the working of the application.
- Modify both the files in such a way that the application is no more vulnerarble.
```

## Solution
Here when I opened the two files, what I first saw that it was using pickle to serialize and deserialize the data,
and in [Official Python Documentation](https://docs.python.org/3/library) it is mentioned that:
```
Warning The pickle module is not secure. Only unpickle data you trust.
It is possible to construct malicious pickle data which will execute arbitrary code during unpickling. Never unpickle data that could have come from an untrusted source, or that could have been tampered with.

Consider signing data with hmac if you need to ensure that it has not been tampered with.

Safer serialization formats such as json may be more appropriate if you are processing untrusted data. See Comparison with json.
```
For refrence [Click Here](https://docs.python.org/3/library/pickle.html)
