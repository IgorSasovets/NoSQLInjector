# NoSQLInjector
Test your MEAN stack app for NoSQL injection. NoSQLInjector is a simple
proxy tool, written on python. It automatically performs NoSQL injection into
request query parameters or request payload. To start using it just redirect requests
to the target server through proxy.

Usage
=====
```
usage: nosqlinjector.py [-h] [-qs INJECTQS] [-p PORT]

Perform NoSQL injection scan

optional arguments:
  -h, --help            show this help message and exit
  -qs INJECTQS, --injectqs INJECTQS
                        inject malicious payload into query string parameters
  -p PORT, --port PORT  proxy port

```

Example
=======
```
python nosqlinjector.py -qs true -p 8081 
```

References
==========
Setup simple proxy using python [tutorial](https://null-byte.wonderhowto.com/how-to/sploit-make-proxy-server-python-0161232/)