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

Also the given was analyzed using the [bandit](https://pypi.org/project/bandit/)

So what we can infer that `pickle.loads` is not a safe function, and if we pickle (unserialize) some untrusted data then a arbitary code execution can happen, which is dangerous.

According to a [Stackoverflow Answer](https://stackoverflow.com/questions/25353753/python-can-i-safely-unpickle-untrusted-data)
```
What does the pickle protocol allow an attacker to do?
Pickle allows classes to customize how their instances are pickled. During the unpickling process, we can:

Call (almost) any class's __setstate__ method (as long as we manage to unpickle an instance of that class).
Invoke arbitrary callables with arbitrary arguments, thanks to the __reduce__ method (as long as we can gain access to the callable somehow).
Invoke (almost) any unpickled object's append, extend and __setitem__ methods, once again thanks to __reduce__.
Access any attribute that Unpickler.find_class allows us to.
Freely create instances of the following types: str, bytes, list, tuple, dict, int, float, bool. This is not documented, but these types are built into the protocol itself and don't go through Unpickler.find_class.
The most useful (from an attacker's perspective) feature here is the ability to invoke callables. If they can access exec or eval, they can make us execute arbitrary code. If they can access os.system or subprocess.Popen they can run arbitrary shell commands. Of course, we can deny them access to these with Unpickler.find_class. But how exactly should we implement our find_class method? Which functions and classes are safe, and which are dangerous?

An attacker's toolbox
Here I'll try to explain some methods an attacker can use to do evil things. Giving an attacker access to any of these functions/classes means you're in danger.

Arbitrary code execution during unpickling:
exec and eval (duh)
os.system, os.popen, subprocess.Popen and all other subprocess functions
types.FunctionType, which allows to create a function from a code object (can be created with compile or types.CodeType)
typing.get_type_hints. Yes, you read that right. How, you ask? Well, typing.get_type_hints evaluates forward references. So all you need is an object with __annotations__ like {'x': 'os.system("rm -rf /")'} and get_type_hints will run the code for you.
functools.singledispatch. I see you shaking your head in disbelief, but it's true. Single-dispatch functions have a register method, which internally calls typing.get_type_hints.
... and probably a few more
Accessing things without going through Unpickler.find_class:

Just because our find_class method prevents an attacker from accessing something directly doesn't mean there's no indirect way of accessing that thing.

Attribute access: Everything is an object in python, and objects have lots of attributes. For example, an object's class can accessed as obj.__class__, a class's parents can be accessed as cls.__bases__, etc.
getattr
operator.attrgetter
object.__getattribute__
Tools.scripts.find_recursionlimit.RecursiveBlowup5.__getattr__
... and many more
Indexing: Lots of things are stored in lists, tuples and dicts - being able to index data structures opens many doors for an attacker.

operator.itemgetter

list.__getitem__, dict.__getitem__, etc

... and almost certainly some more
See Ned Batchelder's Eval is really dangerous to find out how an attacker can use these to gain access to pretty much everything.

Code execution after unpickling:

An attacker doesn't necessarily have to do something dangerous during the unpickling process - they can also try to return a dangerous object and let you call a dangerous function on accident. Maybe you call typing.get_type_hints on the unpickled object, or maybe you expect to unpickle a CuteBunny but instead unpickle a FerociousDragon and get your hand bitten off when you try to .pet() it. Always make sure the unpickled object is of the type you expect, its attributes are of the types you expect, and it doesn't have any attributes you don't expect it to have.

At this point, it should be obvious that there aren't many modules/classes/functions you can trust. When you implement your find_class method, never ever write a blacklist - always write a whitelist, and only include things you're sure can't be abused.

So what's the answer to the question?
If you really only allow access to bool, str, bytes, bytearray, int, float, complex, tuple, list, dict, set and frozenset then you're most likely safe. But let's be honest - you should probably use JSON instead.

In general, I think most classes are safe - with exceptions like subprocess.Popen, of course. The worst thing an attacker can do is call the class - which generally shouldn't do anything more dangerous than return an instance of that class.

What you really need to be careful about is allowing access to functions (and other non-class callables), and how you handle the unpickled object.
```
