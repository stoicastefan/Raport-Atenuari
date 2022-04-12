import requests
from bs4 import BeautifulSoup
from utilities.erp import erp 
from utilities.mail import mail
from datetime import date



link_loss  = []
possible_high_att = {}
high_att = {}
very_high_att = {}
buildings_with_att = []

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
            very_high_att[raw.find_all('td')[7].text[6:]] = recive
        elif recive < -30 :
            high_att[raw.find_all('td')[7].text[6:]] = recive
        elif recive <= -28:
            possible_high_att[raw.find_all('td')[7].text[6:]] = recive

        if status == 0 or status == 4 :
            link_loss.append(raw.find_all('td')[7].text[6:  ])


    bodyPage = soup.body
    bodyPage.table.decompose()
    stats = bodyPage.text.strip()
    stats = stats.replace('\n', '\n|-\n| ')

    f.write(f'\n|-\n| {stats}')

    f.write('\n|}')
    

# Deschide o sesiune cu care ne logam in ERP din care luam datele clientilor

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

        # Deschidem deranjament pentru link loss
        for mac_onu in link_loss:
            client = erp(mac_onu, s)
            contract = client.get_contract()
            location = client.get_location()

            if(contract == None):
                print(f'Nu s-a putut gasi contractul cu Mac ONU {mac_onu}, vezi in Fiber!(daca e contractul de teste nu-i deschidem deranjament)')
            elif(contract != '655000025'):
                print(f'Contractul clientului cu Mac ONU: {mac_onu} este {contract} in locatia {location} (link loss)') 
                mail.open_deranjament('Link loss from ANM', contract )    
                print(f'Deranjament deschis pentru contractul: {contract}')   

        #Verificam daca un client cu atenuare mare are atenuarea individual
        # sau pe cladire iar daca e individual deschidem deranjament 
        for mac_onu in high_att:

            client = erp(mac_onu, s)
            contract = client.get_contract()
            location = client.get_location()
            neighbours = client.get_neighours_mac_onu(location)
            attenuations_of_neighbours = {}
            
            if location not in  buildings_with_att:

                if(len(neighbours) > 1 ):
                    for neighbour in neighbours:
                        if(neighbour in high_att.keys()):
                            attenuations_of_neighbours[neighbour] = high_att[neighbour]
                           
                        
                        elif(neighbour in possible_high_att.keys()):
                            attenuations_of_neighbours[neighbour] = possible_high_att[neighbour]
                            

                        elif(neighbour in very_high_att.keys()):
                            attenuations_of_neighbours[neighbour] = very_high_att[neighbour]
                        else:
                            attenuations_of_neighbours[neighbour] = 0
                        

                    if(max(attenuations_of_neighbours.values()) - min(attenuations_of_neighbours.values()) <= 2.5):
                            buildings_with_att.append(location)
                            print(f'atenuare pe cladirea {location}')
                            mail.open_deranjament_attbuilding(location)
                            continue
                    else:
                        print(f'Contractul clientului cu Mac ONU:  {mac_onu} este {contract} in locatia {location} (high att)')
                elif(contract != '654000025'):
                    print(f'Contractul clientului cu Mac ONU:  {mac_onu} este {contract} in locatia {location} (high att)')

        # Deschidem deranjament cu link loss pentru clientii cu atenuare peste 33.5
        for mac_onu in very_high_att:

            client = erp(mac_onu, s)
            contract = client.get_contract()
            location = client.get_location()
            
            
            if(contract == None):
                print(f'Nu s-a putut gasi contractul cu Mac ONU {mac_onu}, vezi in Fiber!(daca e contractul de teste nu-i deschidem deranjament)')
            elif(contract != '655000025'):
                print(f'Contractul clientului cu Mac ONU: {mac_onu} este {contract} in locatia {location} (link loss)') 
                mail.open_deranjament('Link loss from ANM', contract )    
                print(f'Deranjament deschis pentru contractul: {contract}')

        
                

    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)





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
