from common import open_conf
from optparse import OptionParser
import oauth2
import json
import os
import sys
import check

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
        with open(options.output, 'w') as file1:
            k=json.dump(config1,file1,indent=4)
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
        with open('config_merge', 'w') as file1:
            k=json.dump(config_a,file1,indent=4)
    elif options.check:
        oc1 = open_conf(filename)
        cf1 = oc1['common']
        client = cf1['client_id'],cf1['client_secret']
        tmp1=oc1['items']
        ret3 = []
        for it1 in tmp1:
            try:
                ret2 = check_name(it1,client)
            except ValueError:
                ret2 = 'err :'+ (it1['user']) +'\n'

            if ret2 == '.':
                print (ret2),
            else :
                print ('%'),
                ret3.append(ret2)
            sys.stdout.flush()
        print("\n")
        for it1 in ret3:
            print(it1)

def check_name(config,client):
    client_id,client_secret = client
    user = config['user'].encode('ascii')
    refresh_token = config['refresh_token'].encode('ascii')
    response = oauth2.RefreshToken(client_id, client_secret, refresh_token)

    access_token = response['access_token']
    auth_string = oauth2.GenerateOAuth2String(user, access_token,
                             base64_encode=False)
    ret1, print_mail = check.check(auth_string)
    if ret1 > 0:
        ret2 =  '\n' + config['user']+'\n'+print_mail
    else:
        ret2 = '.'
    return ret2

if __name__ == '__main__':
    main()
