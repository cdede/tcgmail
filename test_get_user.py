#!/usr/bin/env python
import pexpect
import getpass
import re

NAME = 'test.36'

pass1 = getpass.getpass()

def get_user(name):
    return get_two('u',name)

def get_pass(name):
    return get_two('p',name)

def get_two(flag,name):
    p=pexpect.spawn('pwsafe -%sE '%(flag)+name)

    i=p.expect(['Enter passphrase for .*',pexpect.EOF])
    if i==0:
        p.sendline(pass1)
    tmp1 = [line for line in p.readlines() if name in line][0]
    re_com = '.*for %s: (.+)\r' % (name)
    re1 = re.compile(re_com)
    re2 = re1.match(tmp1)
    if re2 :
        return re2.groups()[0]

print len(get_user(NAME))
print get_pass(NAME)
