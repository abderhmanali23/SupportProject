import sys
from os import listdir
from requests import Session
from problemsCount import count
from login import login
from contest_attendance import contest_attendance
from session_attendance import session_attendance
from updateSheet import contest_att,session_att,Sheet_count

session = Session()
sys.stdout = open("output.txt", "w",encoding='utf-8')
sys.stderr = open("error.txt", "w")
handles_file = open("handles.txt","r")
links_file = open("links.txt","r")
Names_file = open("names.txt","r")
input_file = open("input.txt","r")

inputData = input_file.readlines()
Links = links_file.readlines()
sheetsGroupLink = Links[0].rstrip('\n')
contestGroupLink = Links[1].rstrip('\n')
def check_files(file):
    files = listdir()
    if not file in files:
        return False
    return True

def get_handles(handles_file):
    handles = set()
    for hanlde in handles_file.readlines():
        handles.add(hanlde.rstrip('\n').lower())
    return handles

Names = get_handles(Names_file)
handles = get_handles(handles_file)
#user,password = inputData[0].rstrip('\n').split()  
numberOfProblems = 1; numberOfSheet = 1; numberOfContest = 1
Files =  ['updateSheet.py','session_attendance.py','contest_attendance.py','login.py','problemsCount.py','support doc.xlsx']

if not login("The_God_Father","Abderhman.3",session):
            print("Check login information")
            quit()
for file in Files:
    if not check_files(file):
        print(f"{file} file doesn't exist")
        quit()

for require in inputData[1:]:
    lst = require.rstrip('\n').split()
    if lst[0] == 'sheet':
        numberOfProblems = int(lst[1])
        numberOfSheet = int(lst[2])
        info = count(numberOfProblems,numberOfSheet,session,handles,sheetsGroupLink)
        Sheet_count('support doc.xlsx',info,numberOfSheet,numberOfProblems)
    
    elif lst[0] == 'session':
        numberOfWeek = int(lst[1])
        ok = check_files('session.csv')
        if not ok:
            print(f"{ok} file doesn't exist")
            quit()

        info = session_attendance('session.csv',Names)
        session_att('support doc.xlsx',info,numberOfWeek)
    
    elif lst[0] == 'contest':
        numberOfContest = int(lst[1])
        info = contest_attendance(session,numberOfContest,contestGroupLink,handles)
        contest_att('support doc.xlsx',info,numberOfContest)

handles_file.close()
links_file.close()
Names_file.close()
input_file.close()