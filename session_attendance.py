from bs4 import BeautifulSoup
import csv
import pandas as pd

def session_attendance(file,Names:set):
    data = []
    with open(file, 'r',encoding='utf-16') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            data.append(row)
    
    namesInSheet = set()
    Duration_forName = {}

    data = data[8:]
    index = 0
    for conflictRow in data:
        row = []
        for element in conflictRow:
            for seperate in element.split('\t'):
                row.append(seperate)

        data[index] = row
        index += 1

    for i in data:
        namesInSheet.add(i[0].rstrip(' (Guest)'))
        duration = i[5]
        duration_eval = []
        tmp = ""
        for j in duration:
            if j == 'h':
                tmp += '*60'
                duration_eval.append(eval(tmp))
                tmp = ""
            elif j == 'm':
                duration_eval.append(int(tmp))
                tmp = ""
            elif j == 's'or j == " ":
                continue
            else:
                tmp += j

        duration = sum(duration_eval)

        if i[0] in Duration_forName:
            Duration_forName[i[0]] += duration
        else:
            Duration_forName[i[0]] = duration
        
    attendece = {}
    for Name in Names.difference(namesInSheet):
        attendece[Name] = False
    
    for Name in Names.intersection(namesInSheet):
        attendece[Name] = False if Duration_forName[Name] < 30 else True
    
    return attendece
