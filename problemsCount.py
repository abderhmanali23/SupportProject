from bs4 import BeautifulSoup

def count(numberOfProblems, numberOfWeek,session,handles,sheetsGroupLink):
    return num_of_solved_problems(numberOfProblems,numberOfWeek,session,sheetsGroupLink, handles)


def num_of_solved_problems(numberOfProblems:int, numberOfWeek : int, session,sheetsGroupLink, handles:set = {}):
    solvedForEach = {handle : 0 for handle in handles}
    sheetLink = get_sheetLink(session, sheetsGroupLink, numberOfWeek)
    if not sheetLink:
        return False
    AllProblems = solved_prblems(sheetLink, numberOfProblems, session)
    for problem in AllProblems:
        for handle in AllProblems[problem].intersection(handles):
            solvedForEach[handle] += 1
    return solvedForEach

def get_sheetLink(session, sheetsGroupLink, numberOfWeek):
    request = session.get(sheetsGroupLink)
    sheets = BeautifulSoup(request.content, 'html.parser')
    weeks = sheets.find_all('tr',{'class':'highlighted-row'})
    ln = len(weeks)
    if numberOfWeek > ln:
        return False
    
    SheetID = "/" + weeks[ln-numberOfWeek]['data-contestid']
    return sheetsGroupLink[:-1] + SheetID

def solved_prblems(sheetLink, numberOfProblems, session):
    more = ''
    ordinary = 65
    startingPoint = f"/status/{more}{chr(ordinary)}"
    problems = dict()
    while numberOfProblems:
        ok = solved_for_each_problem(sheetLink + startingPoint, session)
        problems[more+chr(ordinary)] = ok
        numberOfProblems -= 1
        ordinary += 1
        if ordinary > 90:
            ordinary = 65
            more = 'Z'
        startingPoint = f"/status/{more}{chr(ordinary)}"
    return problems


def solved_for_each_problem(problemLink, session):
    page = 1
    tmp = ""
    ok = set()
    t = 9
    while t:
        request = session.get(problemLink+f"/page/{page}")
        soup = BeautifulSoup(request.content, 'html.parser')
        if tmp == soup :
            break
        tmp = request
        page += 1
        t -= 1
        body = soup.find('table',{'class':'status-frame-datatable'})
        submissions = body.find_all('tr')
        for submission in submissions[1:]:
            try:
                status = submission.find('span',{'class':'submissionVerdictWrapper'})['submissionverdict']
            except:
                break
            if status == 'OK':
                ok.add(submission.find('a').text.lower())
    return ok



