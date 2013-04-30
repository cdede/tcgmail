from common import open_conf
from optparse import OptionParser
import oauth2
import json
import os
import imaplib
MAX_FETCH = 20
import sys
import email

def arg_parse():
    "Parse the command line arguments"
    parser = OptionParser()
    parser.add_option('-f','--filename', help='conf filename'
            , default='')
    parser.add_option('-a','--add', action='store_true',default=False, 
                        help='add mail conf' )
    parser.add_option('-o','--output', help='output filename'
            , default='config')
    parser.add_option('-m','--merge', action='store_true',default=False, 
                        help='merge  confs to conf' )
    parser.add_option('-c','--check', action='store_true',default=False, 
                        help='check mail' )
    parser.add_option('-u','--username', help='gmail username'
            , default='')
    return parser.parse_args()

def main():
    (options,args) = arg_parse()
    if options.filename == '':
        pass
    else:
        filename = options.filename
    if options.add:
        config1={}
        config1['user']= options.username
        tmpc = open_conf(filename)
        print '  %s' % oauth2.GeneratePermissionUrl(tmpc['client_id'] )
        authorization_code = raw_input('Enter verification code: ')
        response = oauth2.AuthorizeTokens(tmpc['client_id'], tmpc['client_secret'],
                                authorization_code)
        config1['refresh_token']= response['refresh_token']
        file1 = open(options.output, 'w')
        k=json.dump(config1,file1,indent=4)
        file1.close()
        print '\nconfig written.\n'
    elif options.merge:
        config_a ={} 
        cf1 = open_conf(filename)
        config_a['common'] = cf1
        config1=[]
        for f1 in args:
            tmp1=open_conf(f1)
            config1.append(tmp1)

        config_a['items'] = config1
        file1 = open('config_merge', 'w')
        k=json.dump(config_a,file1,indent=4)
        file1.close()
    elif options.check:
        oc1 = open_conf(filename)
        cf1 = oc1['common']
        client = cf1['client_id'],cf1['client_secret']
        tmp1=oc1['items']
        check_items(tmp1,client)

def check_items(tmp1,client):
    for it1 in tmp1:
        num = check_name(it1,client)
        if not num > 0 :
            print '.',
            sys.stdout.flush()

def check_name(config,client):
    client_id,client_secret = client
    user = config['user'].encode('ascii')
    refresh_token = config['refresh_token'].encode('ascii')
    response = oauth2.RefreshToken(client_id, client_secret, refresh_token)

    access_token = response['access_token']
    auth_string = oauth2.GenerateOAuth2String(user, access_token,
                             base64_encode=False)
    imap_conn = imaplib.IMAP4_SSL('imap.gmail.com')
    imap_conn.authenticate('XOAUTH2', lambda x: auth_string)
    imap_conn.select('INBOX', readonly=True)
    _, data = imap_conn.search(None, 'UNSEEN')
    unreads = data[0].split()
    lenunre = len(unreads)
    if lenunre>0:
        print '\n',config['user'],
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
