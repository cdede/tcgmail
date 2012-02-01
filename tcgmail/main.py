'''check gmail
'''
import getpass

from optparse import OptionParser
from pwsafe import Pwsafe
from gmail import Gmail
import sys, os, time
import base64
import tempfile

def check_name(name, pass_a):
    ''' check gmail 
    name = pwsafe name
    pass_a = pwsafe password
    '''
    pw1 = Pwsafe(name, pass_a)
    user = pw1.get_user()
    pass1 = pw1.get_pass()
    mail = Gmail(username=user, password=pass1)

    tmp_a = mail.get_mail_count()
    if tmp_a == 0 :
        print "%s Unused: 0" % (name)
    else:
        print "%s %s Unread: %s" % (name, user, tmp_a)

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
    '''main'''
    usage = "usage: %prog [options] username "
    parser = OptionParser(usage=usage)
    parser.add_option("-g", "--get", action="store_true", dest="get",
                      help="get args[0] user and password with xsel", default=False)

    parser.add_option("-s", "--set-pass", action="store_true", dest="set_pass",
                      help="save password to file", default=False)

    parser.add_option("-i", "--in-pass", action="store_true", dest="echo_pass",
                      help="read  password ", default=False)

    (options, args) = parser.parse_args()
    
    if options.set_pass :
        pass_a = getpass.getpass()
        fd,temp_file_name=tempfile.mkstemp()
        os.close(fd)
        f1=open(temp_file_name,'w')
        f1.write(pass_a) 
        f1.close()
        print temp_file_name
        sys.exit()

    if len(args) < 1:
        parser.error("Please supply username ")

    if options.echo_pass:
        for line in sys.stdin.readlines():
            pass_a = line.replace('\n','')
            break
    else:
        pass_a = getpass.getpass()

    if options.get :
        name = args[0]
        get_name(name, pass_a)
        sys.exit()
    tmp_a = args
    for name in tmp_a:
        check_name(name, pass_a)

