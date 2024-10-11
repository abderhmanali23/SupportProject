from bs4 import BeautifulSoup

def contest_attendance(session,numberOfContest ,contestGroupLink, handles:set = {}):
    Link = get_contestLink(session, numberOfContest, contestGroupLink)
    if not Link:
        return False
    handles.intersection_update(get_attendence(session,Link))
    return handles


def get_contestLink(session,numberOfContest, contestGroupLink):
    request = session.get(contestGroupLink)
    contests = BeautifulSoup(request.content, 'html.parser')
    weeks = contests.find_all('tr',{'class':'highlighted-row'})
    ln = len(weeks)
    if numberOfContest >= ln:
        return False
    
    contestID = "/" + weeks[ln-numberOfContest]['data-contestid']
    return contestGroupLink[:-1] + contestID

def get_attendence(session,contestLink):
    standing = contestLink + "/standings"
    requset = session.get(standing)
    soup = BeautifulSoup(requset.content, 'html.parser')
    part = soup.find('table',{'class':'standings'}).find_all('tr')
    regestered = set()
    for t in part[1:-1]:
        regestered.add(t.find('a').text.lower())
    
    return regestered
