import urllib2
import feedparser
import pexpect
import getpass
import re

from optparse import OptionParser

class Pwsafe:
    def __init__(self, username, password):
        self.pass1 = password
    
    def get_user(self,name):
        return self.get_two('u',name)
    
    def get_pass(self,name):
        return self.get_two('p',name)
    
    def get_two(self,flag,name):
        p=pexpect.spawn('pwsafe -%sE '%(flag)+name)
    
        i=p.expect(['Enter passphrase for .*',pexpect.EOF])
        if i==0:
            p.sendline(self.pass1)
        tmp1 = [line for line in p.readlines() if name in line][0]
        re_com = '.*for %s: (.+)\r' % (name)
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
        file = opener.open(self.url)
        return file.read()

    def _parse_atom(self):
        """ Open feed and parse atom using feedparser
        """
        file = self._open_url()
        self.doc = feedparser.parse(file)

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
#                summaries[x] = {'from_address': entries[x]['author_detail']['email'],
#                    'from_name': entries[x]['author_detail']['name'],
#                    'title': entries[x]['title_detail']['value']}
#        return summaries


if __name__ == "__main__":
    usage = "usage: %prog [options] username "
    parser = OptionParser(usage=usage)
    parser.add_option("-m", "--messages", action="store_true", dest="messages",
                      help="display message information", default=False)

    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.error("Please supply username ")

    name=args[0]
    pass_a = getpass.getpass()
    pw1 = Pwsafe('',pass_a)
    user=pw1.get_user(name)
    pass1= pw1.get_pass(name)
    mail = Gmail(username=user, password=pass1)

    print "Unread: %s" % mail.get_mail_count()
