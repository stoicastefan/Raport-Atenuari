import requests
from bs4 import BeautifulSoup
from utilities.erp import erp 
from utilities.mail import mail
from datetime import date
from collections import OrderedDict



link_loss  = []
possible_high_att = {}
high_att = {}
very_high_att = {}
link_loss_sort = {}
buildings_with_att = []

f = open("AllactivatedONUs.html", "r")
source = f.read()

soup = BeautifulSoup(source , 'lxml')

#Scriem raportul de atenuare in fisierul srcFile intr-un format potrivit pentru wiki

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
        print('----------------------   LINK LOSS  --------------------')
        for mac_onu in link_loss:
            client = erp(mac_onu, s)
            link_loss_sort[mac_onu] =  client.get_pon()
            

        OrderedDict(link_loss_sort)
        for mac_onu in link_loss_sort:
            client = erp(mac_onu, s)
            print(f' Clientul cu locatia: {client.get_location()} si pon: {link_loss_sort[mac_onu]} este link_loss')
        print('------------------------------------------------------- ')
        print(f'Vrei sa deschizi deranjament la {len(link_loss)} clienti cu link loss? (y/n)')
        confirmation = str(input())
        if(confirmation == 'y'):
            for mac_onu in link_loss:
                
                client = erp(mac_onu, s)
                contract = client.get_contract()
                location = client.get_location()

                if(contract == None):
                    print(f'Nu s-a putut gasi contractul cu Mac ONU {mac_onu}, vezi in Fiber!(daca e contractul de teste nu-i deschidem deranjament)')
                elif(contract != '655000025'):
                    print(f'Contractul clientului cu Mac ONU: {mac_onu} este {contract} in locatia {location} (link loss)') 
                    #mail.open_deranjament('Link loss from ANM', contract )    
                    print(f'Deranjament deschis pentru contractul: {contract}')   
            else :
                pass

        #Verificam daca un client cu atenuare mare are atenuarea individual
        # sau pe cladire iar daca e individual deschidem deranjament 
        
        high_att = OrderedDict(high_att)
        
        print('----------------------   HIGH ATT  --------------------')
        for mac_onu in high_att:
            client = erp(mac_onu, s)
            print(f'Clientul cu locatia: {client.get_location()} si pon: {client.get_pon()} are atenuarea: {high_att[mac_onu]}')
        print('---------------------- --------------------------------')
        print(f'Cate deranjamente pentru atenuari deschid(sunt {len(high_att)})')
        numar_atenuari = int(input())

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
                            #mail.open_deranjament_attbuilding(location)
                            continue
                    else:
                        if(numar_atenuari > 0):
                            #mail.open_deranjament('High att', contract )
                            numar_atenuari = numar_atenuari-1
                            --numar_atenuari
                            print(f'Am deschid deranjament pentru  Mac ONU:  {mac_onu} cu contractul: {contract} in locatia {location} (high att)')
                        
                elif(contract != '654000025'):
                    if(numar_atenuari > 0):
                            #mail.open_deranjament('High att', contract )
                            numar_atenuari = numar_atenuari-1
                            --numar_atenuari
                            print(f'Am deschid deranjament pentru  Mac ONU:  {mac_onu} cu contractul: {contract} in locatia {location} (high att)')

        # Deschidem deranjament cu link loss pentru
        # clientii cu atenuare peste 33.5
        for mac_onu in very_high_att:

            client = erp(mac_onu, s)
            contract = client.get_contract()
            location = client.get_location()
            
            
            if(contract == None):
                print(f'Nu s-a putut gasi contractul cu Mac ONU {mac_onu}, vezi in Fiber!(daca e contractul de teste nu-i deschidem deranjament)')
            elif(contract != '655000025'):
                print(f'Contractul clientului cu Mac ONU: {mac_onu} este {contract} in locatia {location} (link loss)') 
                #mail.open_deranjament('Link loss from ANM', contract )    
                print(f'Deranjament deschis pentru contractul: {contract} (att: {very_high_att[mac_onu]})')

        if (buildings_with_att):
            mail.open_deranjament_attbuilding("\n".join(buildings_with_att))
                

    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print(message)
