import json
import os
import subprocess

def open_conf(filename):
    if os.path.splitext(filename)[1] == '.gpg':
        ret= subprocess.Popen(args='gpg --output - %s' % filename, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0]
        tmp1=json.loads(ret)
    else:
        with open(filename,'r') as file1:
            tmp1 = json.load(file1)
    return tmp1
