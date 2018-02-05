import json

REPORT = "/Users/Chaeyeon/Desktop/report.json" #report 디렉토리
API_CLASS = ["file","registry","internet explorer","user interface","net API","network","ole","process","synchronisation","resource","services","system","certificate","encryption","exception","misc","notification","directory","ui"]
BYTE_API = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S"]
with open(REPORT) as f:
    json_data = json.load(f)
    processes = json_data["behavior"]["processes"]
    for i in range (0, len(processes)):
        if processes[i]["track"] == True:
            api_cnt = len(processes[i]["calls"])

            for j in range(0, api_cnt):
                print(BYTE_API[API_CLASS.index(processes[i]["calls"][j]["category"])])

