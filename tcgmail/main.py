
import email
import email.header
import imaplib
import sys
import os
import glob
import shutil

import xoauth
from optparse import OptionParser
import tempfile

scope = 'https://mail.google.com/'
consumer = xoauth.OAuthEntity('anonymous', 'anonymous')
imap_hostname = 'imap.gmail.com'

MAX_FETCH = 20


def get_access_token(config):

  request_token = xoauth.GenerateRequestToken(
      consumer, scope, nonce=None, timestamp=None,
      google_accounts_url_generator=config.google_accounts_url_generator
      )

  oauth_verifier = raw_input('Enter verification code: ').strip()
  try:
    access_token = xoauth.GetAccessToken(
        consumer, request_token, oauth_verifier, config.google_accounts_url_generator)
  except ValueError:
    print 'Incorrect verification code?'
    sys.exit(1)
  return access_token


def main():
  parser = OptionParser()
  parser.add_option("-c", "--check", action="store_true", dest="check",
                      help="check mail", default=False)
  parser.add_option("-a", "--add", action="store_true", dest="add",
                      help="add mail conf", default=False)
  (options, args) = parser.parse_args()


  if options.add:

    class Config():
      pass
    config = Config()
    config.user = raw_input('Please enter your email address: ')
    config.google_accounts_url_generator = xoauth.GoogleAccountsUrlGenerator(config.user)
    access_token = get_access_token(config)
    config.access_token = {'key': access_token.key, 'secret': access_token.secret}
    f = open('config.py', 'w')
    f.write('user = %s\n' % repr(config.user))
    f.write('access_token = %s\n' % repr(config.access_token))
    f.close()
    print '\n\nconfig.py written.\n\n'
  if options.check:
    path1=os.getenv('XDG_CONFIG_HOME')
    path2=tempfile.mkdtemp()
    sys.path.append(path2)
    for it1 in glob.glob(os.path.join(path1,'tcgmail','*.conf')):
      print os.path.splitext(os.path.basename(it1))[0]
      file4=os.path.join(path2,'config.py')
      shutil.copyfile(it1,file4)
      try:
        import config
      except ImportError:
        class Config():
          pass
        config = Config()
      config=reload(config)
      check_name(config)
    shutil.rmtree(path2)


def check_name(config):
  config.google_accounts_url_generator = xoauth.GoogleAccountsUrlGenerator(config.user)
  access_token = xoauth.OAuthEntity(config.access_token['key'], config.access_token['secret'])
  print config.user

  class ImBad():
    def write(self, msg): pass
  sys.stdout = ImBad()
  xoauth_string = xoauth.GenerateXOauthString(
      consumer, access_token, config.user, 'IMAP',
      xoauth_requestor_id=None, nonce=None, timestamp=None)
  sys.stdout = sys.__stdout__

  imap_conn = imaplib.IMAP4_SSL(imap_hostname)
  imap_conn.authenticate('XOAUTH', lambda x: xoauth_string)
  imap_conn.select('INBOX', readonly=True)
  typ, data = imap_conn.search(None, 'UNSEEN')
  unreads = data[0].split()
  print '%d unread message(s).' % len(unreads)
  ids = ','.join(unreads[:MAX_FETCH])
  if ids:
    typ, data = imap_conn.fetch(ids, '(RFC822.HEADER)')
    for item in data:
      if isinstance(item, tuple):
        raw_msg = item[1]
        msg = email.message_from_string(raw_msg)
        print '\033[1;35m%s\033[0m: \033[1;32m%s\033[0m' % (
            email.header.decode_header(msg['from'])[0][0],
            email.header.decode_header(msg['subject'])[0][0],
            )
  imap_conn.close()
  imap_conn.logout()


if __name__ == '__main__':
  main()
