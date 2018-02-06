#-*-coding:utf-8-*-
import os
import json
import sys
import shutil

DIRECTORY = "/home/seclab/.cuckoo/storage/analyses/"
TARGET_DIR = "/home/seclab/virus_pcap/"

task_list = os.listdir(DIRECTORY)
#for task in task_list:
for task in range(1,30001):
	task_dir_name = DIRECTORY + str(task) + "/"
	task_path = task_dir_name + "dump.pcap"
	report_path = DIRECTORY + str(task) + "/reports/report.json"
	try:
		with open(report_path) as f:
			json_data = json.load(f)
			md5 = json_data["target"]["file"]["name"]
		new_path = TARGET_DIR + md5 + ".pcap"
		shutil.copy(task_path,new_path)
	except:
		continue
