#!/usr/bin/python2
'''get user and password
'''
import pexpect
import re
import getpass
import sys
import os
import time
import base64

class Pwsafe:
    '''get user and password
    '''
    def __init__(self, name, password):
        self.pass1 = password
        self.name = name
    
    def get_user(self):
        '''get user '''
        return self.get_two('u')
    
    def get_pass(self):
        '''get password '''
        return self.get_two('p')
    
    def get_two(self, flag):
        '''get user or password '''
        pe1 = pexpect.spawn('pwsafe -%sE '%(flag)+self.name)
    
        i = pe1.expect(['Enter passphrase for .*', pexpect.EOF])
        if i == 0:
            pe1.sendline(self.pass1)
        tmp1 = [line for line in pe1.readlines() if self.name in line][0]
        re_com = '.*for .*%s.*: (.+)\r' % (self.name)
        re1 = re.compile(re_com)
        re2 = re1.match(tmp1)
        if re2 :
            return re2.groups()[0]
 
def get_name(name, pass_a):
    ''' get name user and password with xsel'''
    pw1 = Pwsafe(name, pass_a)
    user = pw1.get_user()
    pass1 = pw1.get_pass()
    print (user)
    encoded = base64.b64encode(pass1)
    os.system('echo %s |base64 -d |xsel -i' % encoded)
    time.sleep(9)
    os.system('xsel -c')

def main(): 
    pass_a = getpass.getpass()
    name = sys.argv[1]
    get_name(name,pass_a)

if __name__ == '__main__':
  main()
