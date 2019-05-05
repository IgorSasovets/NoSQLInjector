# NoSQLInjector
Test your MEAN stack app for NoSQL injection. NoSQLInjector is a simple
proxy tool, written on python. It automatically performs NoSQL injection into
request query parameters or request payload. To start using it just redirect requests
to the target server through proxy.

Usage
=====
```
================================================================================
*  ||    ||  ____  //==\\//==\\||    || ___      __             ____  ______   *
*  ||\\  ||//    \\\\__  ||  ||||    ||||  ||||//  \\|| / ||  //    \\||   \\  *
*  ||  \\||||    ||    \\||  ||||    ||||  ||||||==//||/ =||= ||    ||||       *
*  ||    ||\\____//\\==//\\==\\||====||||  ||||\\__  || \ \\__\\____//||       *
*                                           _//                                *
================================================================================
usage: nosqlinjector.py [-h] [-qs INJECTQS] [-p PORT] [-host PROXYHOST]

Perform NoSQL injection scan

optional arguments:
  -h, --help            show this help message and exit
  -qs INJECTQS, --injectqs INJECTQS
                        inject malicious payload into query string parameters
  -p PORT, --port PORT  proxy port
  -host PROXYHOST, --proxyhost PROXYHOST
                        proxy host
```

Examples of usage
=================
Start app locally and reassure that it uses http protocol. I'd recommend to run API tests
through proxy but if you don't have them, just start an app on the local machine and
configure the browser to use NoSQLInjector proxy.

```
python nosqlinjector.py -qs true -p 8081 
```

An output example:
```
[*] CREATING QUERY STRING INJECTION QUERIES
[*] INJECTED URL: http://localhost:5000/api/v1/users/5ccf287358068c16f402a674/books?id[$ne]=1234&author[$ne]=King
[*] STATUS CODE: 200
[+] INJECTION SUCCESSFUL

```

References
==========
Setup simple proxy using python [tutorial](https://null-byte.wonderhowto.com/how-to/sploit-make-proxy-server-python-0161232/)