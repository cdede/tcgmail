#!/usr/bin/python2
'''check gmail
'''
import urllib2
import feedparser
import pexpect
import getpass
import re

from optparse import OptionParser

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


def main():
    '''main'''
    usage = "usage: %prog [options] username "
    parser = OptionParser(usage=usage)
    parser.add_option("-s", "--split", action="store_true", dest="split",
                      help="split args[0]", default=False)

    (options, args) = parser.parse_args()
    
    if len(args) < 1:
        parser.error("Please supply username ")

    if options.split :
        tmp_a = args[0].split()
    else:
        tmp_a = args

    pass_a = getpass.getpass()
    for name in tmp_a:
        check_name(name, pass_a)

if __name__ == "__main__":
    main()
