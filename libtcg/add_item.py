from common import open_conf
import argparse
import oauth2
import json
import os
import imaplib
MAX_FETCH = 20
import sys

def arg_parse():
    "Parse the command line arguments"
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--filename', help='conf filename'
            , default='')
    parser.add_argument('-a','--add', action='store_true',default=False, 
                        help='add mail conf' )
    parser.add_argument('-m','--merge', action='store_true',default=False, 
                        help='merge  confs to conf' )
    parser.add_argument('-c','--check', action='store_true',default=False, 
                        help='check mail' )
    parser.add_argument('-u','--username', help='gmail username'
            , default='')
    parser.add_argument('filenames', metavar='filename', type=str, nargs='+',                                
                     help='merge filename ')
    return parser.parse_args()

def main():
    args = arg_parse()
    if args.filename == '':
        pass
    else:
        filename = args.filename
    if args.add:
        config1={}
        config1['user']= args.username
        client_id,client_secret = open_conf(filename)
        print '  %s' % oauth2.GeneratePermissionUrl(client_id )
        authorization_code = raw_input('Enter verification code: ')
        response = oauth2.AuthorizeTokens(client_id, client_secret,
                                authorization_code)
        config1['access_token']= response['access_token']
        file1 = open('config', 'w')
        k=json.dump(config1,file1,indent=4)
        file1.close()
        print '\nconfig written.\n'
    elif args.merge:
        config1=[]
        for f1 in args.filenames:
            file1 = open(f1,'r')
            tmp1=json.load(file1)
            file1.close()
            config1.append(tmp1)
        file1 = open('config_merge', 'w')
        k=json.dump(config1,file1,indent=4)
        file1.close()
    elif args.check:
        filename=args.filenames[0]
        if os.path.splitext(filename)[1] == '.gpg':
            pass
        else:
            file1 = open(filename,'r')
            tmp1=json.load(file1)
            file1.close()
        check_items(tmp1)

def check_items(tmp1):
    for it1 in tmp1:
        num = check_name(it1)
        if not num > 0 :
            print '.',
            sys.stdout.flush()

def check_name(config):
    user = config['user'].encode('ascii')
    access_token = config['access_token'].encode('ascii')
    print user,access_token
    auth_string = oauth2.GenerateOAuth2String(user, access_token,
                             base64_encode=False)
    imap_conn = imaplib.IMAP4_SSL('imap.gmail.com')
    imap_conn.authenticate('XOAUTH2', lambda x: auth_string)
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
