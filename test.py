import requests
from bs4 import BeautifulSoup
from datetime import date

f = open("AllactivatedONUs.html", "r")
source = f.read()

soup = BeautifulSoup(source , 'lxml')
# Aici o sa stocam raportul de atenuari
open("srcFile", "w").close()
f = open("srcFile", "a")

linkLoss=[]
highAtt = []

# Se ia raporttul de atenuari din all activated onus si se trece in srcFile intr-un format potrivit pentru wiki
f.write('{| class="wikitable collapsible sortable"\n')
raw = soup.find('tr')
f.write(f'! {raw.find("td").text} ')
for el in raw.find_all('td')[1::]:
        f.write(f'  || {el.text}')
for raw in soup.find_all('tr')[1::]:
    f.write(f'\n|-\n| {raw.find("td").text} ')
    index = 0
    for el in raw.find_all('td')[1::]:
        f.write(f'  || {el.text}')
    #se testeaza daca statusul e linkLoss si atenuarea in parametri
    status = int(raw.find_all('td')[6].text)
    recive = float(raw.find_all('td')[9].text)
    if recive <= -33.5 :
        linkLoss.append(raw.find_all('td')[7].text)
    elif recive < -30 :
        highAtt.append(raw.find_all('td')[7].text)
    if status == 0 or status == 4 :
        linkLoss.append(raw.find_all('td')[7].text)
        
# Se prelucreaza statisticile de la finalul tabelului
bodyPage = soup.body
bodyPage.table.decompose()
stats=bodyPage.text.strip()
stats = stats.split('\n')
stats='\n|-\n| '.join(stats)

f.write(f'\n|-\n| {stats}')

f.write('\n|}')
#f.close()

# Functia primeste mac ONU din tabel si returneaza numarul de contract din ERP
def getContract(macOnu, s):
    try:
        
        source = s.get(f'https://erp.jcs.jo/apartments/manage/?radio_status_nenul=all&filter_location=3&field_location=&filter_code=3&field_code=&filter_contract=3&field_contract=&filter_phone=2&field_phone=&filter_notes=3&field_notes=&filter_status_retea=3&field_status_retea=&filter_package=3&field_package=&filter_odf_port=3&field_odf_port=&filter_pon=3&field_pon=&filter_mac=3&field_mac=&filter_onu_mac=3&field_onu_mac={macOnu}&filter_ip=3&field_ip=&filter_status_onu=3&field_status_onu=').text
        soup = BeautifulSoup(source, 'lxml')
        contract = soup.find(class_="contract-number")
        return contract.text
    except AttributeError as e:
        print(f'clientul cu Mac ONU : {macOnu} nu a fost gasit in ERP (asta inseamna ca o sa il cauti de mana in Fiber/ERP si ii faci deranjament sau daca nu il gasesti il anunti pe Dan!')
        return 'Nu am gasit contractul in ERP'

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
        print(f'Statusul login-ului este: {login_request}')
        for macOnu in linkLoss:
            print(f'Contractul clientului {macOnu} este {getContract(macOnu[5::], s)}(link loss)')        
        for macOnu in highAtt:
            print(f'Contractul clientului {macOnu} este {getContract(macOnu[5::], s)}(high att)')
    except Exception as e:
        print('Logarea nu a reusit')


#Adaugam raportul in wiki



# POST request to log in.
S = requests.Session()
URL = 'http://10.1.1.11/mediawiki/api.php'
# Step 3: GET request to fetch CSRF token
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

PARAMS = {
    "action": "edit",
    "title": "Srcc",
    "token": CSRF_TOKEN,
    "format": "json",
    "text": f.read(),
    
}

R = S.post(URL, data=PARAMS)
DATA = R.json()

# Adauga link cu raportul de aenuare in pagina cu rapoarte
PARAMS = {
    "action": "parse",
    "page": "Srccc",
    "prop": "wikitext",
    "format": "json"
}

R = S.get(url=URL, params=PARAMS)
DATA = R.json()

newContent = DATA["parse"]["wikitext"]["*"]
newContent = newContent.split('[' , 0)

today = date.today()
d = today.strftime("%d.%m.%Y")

print(d)


#  POST request to edit a page
PARAMS = {
    "action": "edit",
    "title": "Srccc",
    "token": CSRF_TOKEN,
    "format": "json",
    "text": f'\n\n[[Raport pentru atenuari {d}]]\n\n['.join(newContent),
    
}

R = S.post(URL, data=PARAMS)
DATA = R.json()




