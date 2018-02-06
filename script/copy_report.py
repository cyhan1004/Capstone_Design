#-*-coding:utf-8-*-
import os
import json
import sys
import shutil

DIRECTORY = "/home/seclab/.cuckoo/storage/analyses/"
TARGET_DIR = "/home/seclab/virus_reports/"

task_list = os.listdir(DIRECTORY)
#for task in task_list:
for task in range(1,30001):
	task_dir_name = DIRECTORY + str(task) + "/reports/"
	task_path = task_dir_name + "report.json"
	try:
		with open(task_path) as f:
			json_data = json.load(f)
			md5 = json_data["target"]["file"]["name"]
		new_path = TARGET_DIR + md5 + ".json"
		shutil.copy(task_path,new_path)
	except:
		continue
