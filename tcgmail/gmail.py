'''check gmail
'''
import urllib2
import feedparser
   
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


