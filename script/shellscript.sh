#! /bin/bash

sudo cuckoo &
sleep 20
sudo cuckoo process instance1 & sudo cuckoo process instance2 & sudo cuckoo process instance3 &
sudo cuckoo web -H 203.246.112.138 -p 8080 &
sudo cuckoo api -H 192.168.56.1 -p 8090 &
sudo rm -rf /home/wins/tasklist.pickle
sudo /usr/sbin/cron

