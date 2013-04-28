from common import open_conf
import argparse
import oauth2
import json

def arg_parse():
    "Parse the command line arguments"
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--filename', help='conf filename'
            , default='')
    parser.add_argument('-a','--add', action='store_true',default=False, dest='add',
                        help='add mail conf' )
    parser.add_argument('-c','--check', action='store_true',default=False, dest='check',
                        help='check mail' )
    parser.add_argument('-u','--username', help='gmail username'
            , default='')
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


if __name__ == '__main__':
    main()
