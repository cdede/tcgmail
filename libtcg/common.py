import json
def open_conf(filename):
    file1 = open(filename,'r')
    cf1 = json.load(file1)
    file1.close()
    return cf1['client_id'],cf1['client_secret']
