from bs4 import BeautifulSoup

def getCsrf(URL:str,session):
    auth = session.get(URL).content
    soup = BeautifulSoup(auth, 'html.parser')
    csrf = soup.find('input')['value']
    return csrf

def login(handle, password,session):
    URL = "https://codeforces.com/enter"
    csrf_token_login = getCsrf(URL,session)
    login_data = {
        'action' : 'enter',
        'handleOrEmail' : handle,
        'password' : password,
        'csrf_token' : csrf_token_login,
        'remember' : 'on'
    }

    headers = {
        'X-Csrf-Token' : csrf_token_login
    }

    request = session.post(URL,data=login_data,headers=headers)
    if request.status_code != 200:
        print(request.status_code)
        return False
    return True
