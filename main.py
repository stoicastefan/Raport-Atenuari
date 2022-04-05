import requests
from bs4 import BeautifulSoup
from datetime import date
from smtplib import SMTP_SSL, SMTP_SSL_PORT
from email.message import EmailMessage


link_loss  = []
high_att = []

source = requests.get('http://monitor.jcs.jo/onu/activated_onu.php').text
soup = BeautifulSoup(source, 'lxml')

with open("srcFile", "w") as f:

    f.write('{| class="wikitable collapsible sortable"\n')
    raw = soup.find('tr')
    f.write(f'! {raw.find("td").text} ')
    for el in raw.find_all('td')[1:]:
            f.write(f'  || {el.text}')

    for raw in soup.find_all('tr')[1:]:
        f.write(f'\n|-\n| {raw.find("td").text} ')

        for el in raw.find_all('td')[1:]:
            f.write(f'  || {el.text}')

        status = int(raw.find_all('td')[6].text)
        recive = float(raw.find_all('td')[9].text)

        if recive <= -33.5 :
            link_loss.append(raw.find_all('td')[7].text)
        elif recive < -30 :
            high_att.append(raw.find_all('td')[7].text)

        if status == 0 or status == 4 :
            link_loss.append(raw.find_all('td')[7].text)


    bodyPage = soup.body
    bodyPage.table.decompose()
    stats = bodyPage.text.strip()
    stats = stats.replace('\n', '\n|-\n| ')

    f.write(f'\n|-\n| {stats}')

    f.write('\n|}')



# Deschide o sesiune cu care ne logam in ERP din care luam numarul de contract clientilor
with requests.Session() as s:
    s.get('https://erp.jcs.jo/login/')
    login_csrftoken = s.cookies['csrftoken']
    login_data = {
        'username': 'stefan',
        'password': 'stefan112',
        'csrfmiddlewaretoken': login_csrftoken
    }

    login_request = (
        s.post(
            url='https://erp.jcs.jo/login/',
            data=login_data,
            headers=dict(Referer='https://erp.jcs.jo/login/')
        )
    )

    soup = BeautifulSoup(login_request.text, 'lxml')    
    try:
        if(soup.find('title').text == 'Login - JCS ERP'):
            raise Exception

        for mac_onu in link_loss:
            contract = get_contract(mac_onu[5:], s)
            if(contract == None):
                print(f'Nu s-a putut gasi contractul cu Mac ONU {mac_onu}, vezi in Fiber!(daca e contractul de teste nu-i deschidem deranjament)')
            elif(contract != '655000025'):
                print(f'Contractul clientului cu Mac ONU: {mac_onu} este {contract}(link loss)') 
                #open_deranjament('Link loss from ANM', contract )    
                print(f'Deranjament deschis pentru contractul: {contract}')   

        for mac_onu in high_att:
            contract = get_contract(mac_onu[5:], s)
            if(contract != '655000025'):
                print(f'Contractul clientului cu Mac ONU:  {mac_onu} este {contract}(high att)')
    except Exception as e:
        print('Logarea nu a reusit')




#Adaugam raportul in wiki



# POST request pentru log in.
S = requests.Session()
URL = 'http://10.1.1.11/mediawiki/api.php'
# Step 3: GET request pentru a lua CSRF token
PARAMS = {
    "action": "query",
    "meta": "tokens",
    "format": "json"
}

R = S.get(url = URL, params=PARAMS)
DATA = R.json()

CSRF_TOKEN = DATA['query']['tokens']['csrftoken']

# Adauga tabelul cu raportul de atenuari

f = open("srcFile", "r")

today = date.today()
d = today.strftime("%d.%m.%Y")

PARAMS = {
    "action": "edit",
    "title": f"Raport pentru atenuari {d}",
    "token": CSRF_TOKEN,
    "format": "json",
    "text": f.read(),
    
}

R = S.post(URL, data=PARAMS)
DATA = R.json()

# Adauga link cu raportul de atenuare in pagina cu rapoarte
PARAMS = {
    "action": "parse",
    "page": "Rapoarte_atenuari",
    "prop": "wikitext",
    "format": "json"
}

R = S.get(url=URL, params=PARAMS)
DATA = R.json()

newContent = DATA["parse"]["wikitext"]["*"]
newContent = newContent.split('[' , 1)


#  POST request pentru a edita pagina de wiki
PARAMS = {
    "action": "edit",
    "title": "Rapoarte_atenuari",
    "token": CSRF_TOKEN,
    "format": "json",
    "text": f'\n\n[[Raport pentru atenuari {d}]]\n\n['.join(newContent),
    
}

R = S.post(URL, data=PARAMS)
DATA = R.json()
