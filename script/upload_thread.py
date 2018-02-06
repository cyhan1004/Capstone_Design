#-*-coding:utf-8-*-
#uploading script using thread (frequency : 10 sec)

import requests, os

import time, sys
import multiprocessing as mp

import threading
REST_URL = "http://192.168.56.1:8090/tasks/create/file"
#DIRECTORY = "/home/seclab/KISA_CISC2017-Malware_1st"

def explorer( root ):
    ret = []
    for path, dir, files in os.walk(root) :
        for file in files :
            ret.append(os.path.join(path, file))
    return ret

def get_file_name ( file_path ) :
    return os.path.basename(file_path)

def send_file( file_path ) :
    with open(file_path, 'rb') as f :
        file_name = get_file_name(file_path)
        fs = {'file' : (file_name, f)}
        r = requests.post(REST_URL, files=fs)
        if r.status_code == 200 :
            print("{} is succeeded".format(file_name))
	    os.remove(os.path.join(file_path, file_name))
        else :
            print("{} is failed".format(file_name))

def run( root , process_count = os.cpu_count() ) :
    start = time.time()
    file_path_list = explorer(root)
    mp.freeze_support()
    p = mp.Pool( process_count )
    p.map(send_file, file_path_list)
    print("TIME : {time}".format(time = time.time() - start))
    threading.Timer(10, run, args=[root, process_count]).start()

if __name__ == '__main__' :
    if len(sys.argv) == 2 :
        run(sys.argv[1])
    elif len(sys.argv) == 3 :
        run(sys.argv[1], int(sys.argv[2]))
