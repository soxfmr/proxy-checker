proxy-checker
=============
A simple python script to check if a proxy is working.

This project was forked from [ApsOps/proxy-checker](https://github.com/ApsOps/proxy-checker) but it is the totally refactor version with a few of new features below:

- Mutil-Thread for proxy detecting.
- Retrieve the IPs from local file.

How To Use
=============
1. Replace the file ip.txt in the root folder with the formatted content:
```
192.168.1.3 80
172.10.23.1 8080
```
2. Execute the script and you have done:
```shell
python proxy-checker.py
```

Todo-List
=============
- Export the result
