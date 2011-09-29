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
        re_com = '.*for %s: (.+)\r' % (self.name)
        re1 = re.compile(re_com)
        re2 = re1.match(tmp1)
        if re2 :
            return re2.groups()[0]
    
class Gmail:
    """ Provides interface for checking Google Mail
        For use with Conky
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.url = 'https://mail.google.com/mail/feed/atom'
        self.passwd_mgr = self._password_manager()
        self.doc = None

    def _password_manager(self):
        """ Build and return a password manager
        """
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, self.url, self.username, self.password)
        return password_mgr

    def _open_url(self):
        """ Using password manager open and read feed url over https
        """
        handler = urllib2.HTTPBasicAuthHandler(self.passwd_mgr)

        opener = urllib2.build_opener(handler)
        file1 = opener.open(self.url)
        return file1.read()

    def _parse_atom(self):
        """ Open feed and parse atom using feedparser
        """
        file1 = self._open_url()
        self.doc = feedparser.parse(file1)

    def get_mail_count(self):
        """ Return unread mail count
        """
        self._parse_atom()
        return len(self.doc['entries'])

    def get_mail_summary(self, number=3):
        """ Return summary of emails, containing from and subject
        """
        pass
#        entries = doc.entries
#        summaries = {}
#        if entries:
#            for x in range(3):
#                summaries[x] = {
#                    'from_address': entries[x]['author_detail']['email'],
#                    'from_name': entries[x]['author_detail']['name'],
#                    'title': entries[x]['title_detail']['value']}
#        return summaries


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
