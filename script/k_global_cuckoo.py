#-*- coding: utf-8 -*-

# Script2 : cuckoo 서버 -> wins 서버로 malware 보내기

import paramiko
import os, os.path
import json
import time, sys
import shutil
import multiprocessing as mp
import threading
import requests
import pickle

REST_URL = "http://192.168.56.1:8090/tasks/create/file"

DIRECTORY_REPORT_ORIGINAL = "/home/seclab/.cuckoo/storage/test_analyses" #원래 리포트가 저장되는 디렉토리(detect)
ANALYZE_DIRECTORY = "/home/wins/not_analyze" # 쿠쿠 코어에 업로드할 파일(detect)
TARGET_DIRECTORY = "/home/wins/analyze" # 리포트파일 디렉토리(detect)
WINS_IP = "112.168.216.205"
WINS_PORT = 222
PICKLE = "/home/wins/tasklist2.pickle"

def detectUploadingFile(file_path = ANALYZE_DIRECTORY) :
	file_list = []
	filenames = os.listdir(file_path) #ANALYZE_DIRECTORY
	for file in filenames:
		print(os.path.join(file_path, file))
		full_file_name = os.path.join(file_path, file)
		file_list.append(full_file_name)
	for path in file_list:
		with open(path, "rb") as f:
			file_name = os.path.basename(path)
			if file_name == "not_analyze":
				break
			#path_split_list = path.split('/')
			#file_name = path_split_list[-1]
			fs = {"file": (file_name, f)}
			r = requests.post(REST_URL, files=fs)
			os.remove(path)
	#threading.Timer(3600, detectUploadingFile, args=[file_path]).start()

def detectReportFile(file_path = DIRECTORY_REPORT_ORIGINAL) :
	if not os.path.exists(TARGET_DIRECTORY):
		os.makedirs(TARGET_DIRECTORY)		
	
	#if TASK_NUM == 0:
	#	threading.Timer(3600, detectReportFile, args=[file_path]).start()
	if not os.path.exists(PICKLE):
		previous_set = set()
	else:
		with open(PICKLE, 'rb') as f:
			previous_set = pickle.load(f)
	current_set = set(os.listdir(file_path))
	if len(current_set) == 0:
		return
	#	pickle.dump(set(task_list), f)
	work_set = current_set - previous_set #all files - completed files
	complete_set = previous_set
	pending_list = list() #uploading file list to wins server 
	for task_num in work_set:
		src_file_path = file_path +'/'+ task_num + "/reports/report.json"
		if(os.path.exists(src_file_path)):
			pending_list.append([src_file_path,task_num])
			print("add pending list :\n "+src_file_path)
	success_set = transferFilesToServer(pending_list)
	complete_set = complete_set | success_set
	with open(PICKLE, 'wb') as f :
		pickle.dump(complete_set, f)
	print("finish")

def transferFilesToServer(pending_list):
	transport = paramiko.Transport((WINS_IP, WINS_PORT))
	transport.connect(username="wins", password="wins!!!!")
	sftp = paramiko.SFTPClient.from_transport(transport)
	ret_set = set()
	for file_path, task_num in pending_list:
		with open(file_path,'r') as f:
			json_data = json.load(f)
			md5 = json_data["target"]["file"]["md5"]
			new_path = TARGET_DIRECTORY + "/" + md5 + ".json"
			try:
				sftp.put(file_path, new_path)
				ret_set.add(task_num)
				#os.remove(file_path)	#로컬에 파일 남기기 싫으면 주석 해제
			except Exception as e:
				raise e	
	sftp.close()
	transport.close()
	return ret_set

if __name__ == '__main__' :
	detectUploadingFile(ANALYZE_DIRECTORY)	
	detectReportFile(DIRECTORY_REPORT_ORIGINAL)
	exit()
