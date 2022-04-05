import requests
from bs4 import BeautifulSoup
from datetime import date
from smtplib import SMTP_SSL, SMTP_SSL_PORT
from email.message import EmailMessage

link_loss  = []
high_att = []

f = open("AllactivatedONUs.html", "r")
source = f.read()

soup = BeautifulSoup(source , 'lxml')
# Aici o sa stocam raportul de atenuari
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
    


def open_deranjament(type_deranjament, contract):

    content= f'''Technical
######
Name: NOC ROMANIA
######
Phone: {contract}
######
Email: monitor@jcs.jo
######
Account number: {contract}
######
Message:{type_deranjament}
######
Call back: I want to be called on the number below
                '''
    mail_deranjament = EmailMessage()
    mail_deranjament.add_header('Subject', "New Message From Jordan European Internet")
    mail_deranjament.set_content(content)
    #Ne conectam si trimitem mailul
    smtp_server = SMTP_SSL('mail.jcs.jo', port=SMTP_SSL_PORT)
    smtp_server.login('monitor@jcs.jo', 'tpS#Np^3n3vR6$v5')
    smtp_server.sendmail('monitor@jcs.jo', 'webmaster@jcs.jo', mail_deranjament.as_bytes())
    #Ne deconectam de pe server
    smtp_server.quit()


# Functia primeste mac ONU din tabel si returneaza numarul de contract din ERP
def get_contract(mac_onu, s):
    try:
        
        source = s.get(f"""https://erp.jcs.jo/apartments/manage/
        ?radio_status_nenul=all
        &filter_location=3
        &field_location=
        &filter_code=3
        &field_code=
        &filter_contract=3
        &field_contract=
        &filter_phone=2
        &field_phone=
        &filter_notes=3
        &field_notes=
        &filter_status_retea=3
        &field_status_retea=
        &filter_package=3
        &field_package=
        &filter_odf_port=3
        &field_odf_port=
        &filter_pon=3
        &field_pon=
        &filter_mac=3
        &field_mac=
        &filter_onu_mac=3
        &field_onu_mac={mac_onu}
        &filter_ip=3
        &field_ip=
        &filter_status_onu=3
        &field_status_onu=
        """).text
        soup = BeautifulSoup(source, 'lxml')        

        contract = soup.find_all(class_="contract-number")

        for client in contract:
            if client.text != 'None':
                return client.text
    except AttributeError as e:
        print(f'clientul cu Mac ONU : {mac_onu} nu a fost gasit in ERP (asta inseamna ca o sa il cauti de mana in Fiber/ERP si ii faci deranjament sau daca nu il gasesti il anunti pe Dan!')
        return 'Nu am gasit contractul in ERP'

def get_locatie(mac_onu, s):
    try:
        
        source = s.get(f"""https://erp.jcs.jo/apartments/manage/
        ?radio_status_nenul=all
        &filter_location=3
        &field_location=
        &filter_code=3
        &field_code=
        &filter_contract=3
        &field_contract=
        &filter_phone=2
        &field_phone=
        &filter_notes=3
        &field_notes=
        &filter_status_retea=3
        &field_status_retea=
        &filter_package=3
        &field_package=
        &filter_odf_port=3
        &field_odf_port=
        &filter_pon=3
        &field_pon=
        &filter_mac=3
        &field_mac=
        &filter_onu_mac=3
        &field_onu_mac={mac_onu}
        &filter_ip=3
        &field_ip=
        &filter_status_onu=3
        &field_status_onu=
        """).text
        soup = BeautifulSoup(source, 'lxml')        

        location = soup.find_all(id="Location")

        for client in location:
            if client.text != 'None':
                return client.text
    except AttributeError as e:
        print(f'clientul cu Mac ONU : {mac_onu} nu a fost gasit in ERP (asta inseamna ca o sa il cauti de mana in Fiber/ERP si ii faci deranjament sau daca nu il gasesti il anunti pe Dan!')
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
            locatie = get_locatie(mac_onu[5:], s)
            if(contract != '655000025'):
                print(f'Contractul clientului cu Mac ONU:  {mac_onu} este {contract}(high att) la locatie: {locatie}')
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

today = date.today()
d = today.strftime("%d.%m.%Y")

PARAMS = {
    "action": "edit",
    "title": f"!!!!Raport pentru atenuari {d}",
    "token": CSRF_TOKEN,
    "format": "json",
    "text": f.read(),
    
}

#R = S.post(URL, data=PARAMS)
#DATA = R.json()

# Adauga link cu raportul de aenuare in pagina cu rapoarte
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


#  POST request to edit a page
PARAMS = {
    "action": "edit",
    "title": "Rapoarte_atenuari",
    "token": CSRF_TOKEN,
    "format": "json",
    "text": f'\n\n!!![[Raport pentru atenuari {d}]]\n\n['.join(newContent),
    
}

#R = S.post(URL, data=PARAMS)
#DATA = R.json()