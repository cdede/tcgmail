
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
import os.path
import subprocess

consumer = xoauth.OAuthEntity('anonymous', 'anonymous')

MAX_FETCH = 20


def main():
    parser = OptionParser()
    parser.add_option("-c", "--check", action="store_true", dest="check",
                      help="check mail", default=False)
    (options, args) = parser.parse_args()

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
    for it1 in tmp1:
        class Config():
            pass
        config = Config()
        for key2,item in it1['access_token'].items():
            it1['access_token'][key2]=item.encode('ascii')
        config.user=it1['user'].encode("ascii")
        config.access_token=it1['access_token']
        num = check_name(config)
        if not num > 0 :
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
