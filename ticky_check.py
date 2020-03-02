#!/usr/bin/env python3

import csv
import re
import operator

error = {}
per_user = {}

with open("syslog.log", "r") as files:
    lines = files.readlines()
    for line in lines:
        username = line.split(" ")[-1][1:-2]
        if(re.search(r"ticky: INFO ([\w ]*)", line)!= None):
            if(username in per_user):
                per_user[username][0] += 1
            else:
                per_user[username] = [1,0]
        elif(re.search(r"ticky: ERROR ([\w ]*)", line)!= None):
            if(username in per_user):
                per_user[username][1] += 1
            else:
                per_user[username] = [0,1]
            errors = re.findall(r"ticky: ERROR ([\w ]*) ", line)
            if(errors[0] in error):
                error[errors[0]] += 1
            else:
                error[errors[0]] = 1

files.close()
serror = sorted(error.items(), key = operator.itemgetter(1), reverse=True)
sper_user =sorted(per_user.items(), key = operator.itemgetter(0))

with open("error_message.csv","w") as f1:
    write = csv.writer(f1)
    write.writerow(("Error", "Count"))
    for i in serror:
        write.writerow(i)
f1.close()

with open("user_statistics.csv","w") as f2:
    write = csv.writer(f2)
    write.writerow(("Username", "INFO", "ERROR"))
    for i in sper_user:
        write.writerow([i[0],i[1][0], i[1][1]])
f2.close()
