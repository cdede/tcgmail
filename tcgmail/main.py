
import email
import email.header
import imaplib
import sys
import os
import shutil

import xoauth
from optparse import OptionParser
import tempfile
import json
import time
import os.path
import subprocess

consumer = xoauth.OAuthEntity('anonymous', 'anonymous')

MAX_FETCH = 20


def get_access_token(google_accounts_url_generator):
    scope = 'https://mail.google.com/'

    request_token = xoauth.GenerateRequestToken(
      consumer, scope, nonce=None, timestamp=None,
      google_accounts_url_generator=google_accounts_url_generator
      )

    oauth_verifier = raw_input('Enter verification code: ').strip()
    try:
        access_token = xoauth.GetAccessToken(
        consumer, request_token, oauth_verifier, 
        google_accounts_url_generator)
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
        config2={}
        config1={}
        config1['user']= raw_input('Please enter your email address: ')
        access_token = get_access_token(xoauth.GoogleAccountsUrlGenerator(config1['user']))
        config1['access_token']= {'key': access_token.key, 
                'secret': access_token.secret}
        
        file1 = open('config', 'w')
        config2[str(int(time.time()))]=config1
        k=json.dump(config2,file1,indent=4)
        file1.close()
        print '\n\nconfig written.\n\n'

    if options.check:
        filename=args[0]
        if os.path.splitext(filename)[1] == '.gpg':
            ret= subprocess.Popen(args='gpg --output - %s' % filename, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0]
            tmp1=json.loads(ret)
        else:
            file1 = open(filename,'r')
            tmp1=json.load(file1)
            file1.close()
        check_items(tmp1)

def check_items(tmp1):
    for key,it1 in tmp1.items():
        class Config():
            pass
        config = Config()
        for key2,item in it1['access_token'].items():
            it1['access_token'][key2]=item.encode('ascii')
        config.user=it1['user'].encode("ascii")
        config.access_token=it1['access_token']
        num = check_name(config)
        if num > 0 :
            print key
        else:
            print '.',
            sys.stdout.flush()

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
