# usertk

`UserTk` is a tool for network or site administrators who want to monitor the users activity through squid access log. For example, with `UserTK`, you can implement a quota system for a proxy service.

The idea is to allow pluggins process the data from the SQUID log and do with that information what they want, for example, 
store it in a table or send an email to the administrator.

## Requisites

You must install pydal [https://github.com/web2py/pydal] and the apropiate driver for the database system to be used by usertk.
 
## Install
 
For install:
  
```bash
$ git clone https://github.com/ybenitezf/usertk.git
$ cd usertk
$ sudo python setup.py install
```
  
## Configuration

* Create required directories:
```bash
$ sudo mkdir /etc/usertk
$ sudo mkdir /var/log/usertk
```
* Copy `usertk/usertk/excludes.txt` to `/etc/usertk` and edit it as you felt to be apropiated.
* Create a link to `usertk/usertk/config.py` in `/etc/usertk`. Not necesary but is confortable to have, make the link target the `config.py` installed in the system - not the one in the clone git repository, for example in my Ubuntu:
```bash
$ sudo ln -s /usr/local/lib/python2.7/dist-packages/usertk/core/config.py /etc/usertk/config.py
```
* Create the user and database for `UserTK`.
* Edit `/etc/usertk/config.py` and change the default values to the apropiated ones.
* Normally `Usertk` is mean to be execute with the same user as squid-proxy, so give the apropiated permission to those directories and files to that user.

## Running `UserTK`

To start `UserTK` open a terminal and execute, change `proxy` to the apropiate user if necessary:

```bash
sudo su -m proxy -c usertk-control.py --start
```
To stop `Usertk`:
```bash
sudo su -m proxy -c usertk-control.py --stop
```
And to restart it:
```bash
sudo su -m proxy -c usertk-control.py --restart
```
## Troubleshooting

See `/var/log/usertk/usertk.log`, and change `level` in `/etc/usertk/config.py` to get more verbosity out of `UserTK`
