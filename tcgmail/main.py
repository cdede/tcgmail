
import email
import email.header
import imaplib
import sys
import os
import shutil

import xoauth
from optparse import OptionParser
import tempfile

consumer = xoauth.OAuthEntity('anonymous', 'anonymous')

MAX_FETCH = 20


def get_access_token(config):
    scope = 'https://mail.google.com/'

    request_token = xoauth.GenerateRequestToken(
      consumer, scope, nonce=None, timestamp=None,
      google_accounts_url_generator=config.google_accounts_url_generator
      )

    oauth_verifier = raw_input('Enter verification code: ').strip()
    try:
        access_token = xoauth.GetAccessToken(
        consumer, request_token, oauth_verifier, 
        config.google_accounts_url_generator)
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
        config.google_accounts_url_generator = \
        xoauth.GoogleAccountsUrlGenerator(config.user)
        access_token = get_access_token(config)
        config.access_token = {'key': access_token.key, 
                'secret': access_token.secret}
        file1 = open('config.py', 'w')
        file1.write('user = %s\n' % repr(config.user))
        file1.write('access_token = %s\n' % repr(config.access_token))
        file1.close()
        print '\n\nconfig.py written.\n\n'
    if options.check:
        path2 = tempfile.mkdtemp()
        sys.path.append(path2)
        for it1 in args:
            file4 = os.path.join(path2,'config.py')
            shutil.copyfile(it1, file4)
            try:
                import config
            except ImportError:
                class Config():
                    pass
                config = Config()
            config = reload(config)
            num = check_name(config)
            if num > 0 :
                print os.path.splitext(os.path.basename(it1))[0]
            else:
                print '.',
                sys.stdout.flush()

        shutil.rmtree(path2)


def check_name(config):
    imap_hostname = 'imap.gmail.com'
    config.google_accounts_url_generator = \
            xoauth.GoogleAccountsUrlGenerator(config.user)
    access_token = xoauth.OAuthEntity(config.access_token['key'], 
            config.access_token['secret'])

    class ImBad():
        def write(self, msg): 
            pass
    sys.stdout = ImBad()
    xoauth_string = xoauth.GenerateXOauthString(
          consumer, access_token, config.user, 'IMAP',
          xoauth_requestor_id=None, nonce=None, timestamp=None)
    sys.stdout = sys.__stdout__

    imap_conn = imaplib.IMAP4_SSL(imap_hostname)
    imap_conn.authenticate('XOAUTH', lambda x: xoauth_string)
    imap_conn.select('INBOX', readonly=True)
    _, data = imap_conn.search(None, 'UNSEEN')
    unreads = data[0].split()
    lenunre = len(unreads)
    if lenunre>0:
        print '\n',config.user,
        print '%d unread message(s).' % lenunre
    ids = ','.join(unreads[:MAX_FETCH])
    if ids:
        _, data = imap_conn.fetch(ids, '(RFC822.HEADER)')
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
    return lenunre


if __name__ == '__main__':
    main()
