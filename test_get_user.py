#!/usr/bin/env python
import pexpect
import getpass
NAME = 'test.36'
pass1 = getpass.getpass()
ssh_newkey = 'Are you sure you want to continue connecting'
# my ssh command line
p=pexpect.spawn('pwsafe -uE '+NAME)

i=p.expect(['Enter passphrase for .*',pexpect.EOF])
if i==0:
    p.sendline(pass1)
print p.readlines()
