import json
import os
import subprocess

def open_conf(filename):
    if os.path.splitext(filename)[1] == '.gpg':
        ret= subprocess.Popen(args='gpg --output - %s' % filename, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0]
        tmp1=json.loads(ret)
    else:
        file1 = open(filename,'r')
        tmp1 = json.load(file1)
        file1.close()
    return tmp1
