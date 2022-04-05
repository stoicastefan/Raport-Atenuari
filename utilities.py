from bs4 import BeautifulSoup
from smtplib import SMTP_SSL, SMTP_SSL_PORT
from email.message import EmailMessage


# In clasa erp gasim toate functiile care preiau date din ERP
class erp:

        def get_locatie(mac_onu, s):
            try:
                
                source = s.get('https://erp.jcs.jo/apartments/manage/' \
                '?radio_status_nenul=all'\
                '&filter_location=3' \
                '&field_location='\
                '&filter_code=3'\
                '&field_code='\
                '&filter_contract=3'\
                '&field_contract='\
                '&filter_phone=2'\
                '&field_phone='\
                '&filter_notes=3'\
                '&field_notes='\
                '&filter_status_retea=3'\
                '&field_status_retea='\
                '&filter_package=3'\
                '&field_package='\
                '&filter_odf_port=3'\
                '&field_odf_port='\
                '&filter_pon=3'\
                '&field_pon='\
                '&filter_mac=3'\
                '&field_mac='\
                f'&field_onu_mac={mac_onu}'\
                '&filter_ip=3'\
                '&field_ip='\
                '&filter_status_onu=3'\
                '&field_status_onu='
                ).text
                soup = BeautifulSoup(source, 'lxml')        

                tabel = soup.find('tbody')
                for raw in tabel.find_all('tr'):
                    test = raw.find_all('td')
                    print(f'Elementul pentru {mac_onu} cu lungimea {len(test)}este:----------------------------------------')
                    for el in raw.find_all('td'):
                        print(el.text)
                    #if el[2].text != None and el[4].text != None:
                        #return el[2].text

            except AttributeError as e:
                print(f'clientul cu Mac ONU : {mac_onu} nu a'\
                          'fost gasit in ERP (asta inseamna ca o sa '\
                          'il cauti de mana in Fiber/ERP si ii faci deranjament '\
                          'sau daca nu il gasesti il anunti pe Dan!'\
                     )
                print(e)
                


        # Functia primeste mac ONU din tabel si returneaza numarul de contract din ERP

        def identificare_atenuare_cladire(mac_onu, s):
                try:
                    
                    source = s.get('https://erp.jcs.jo/apartments/manage/' \
                    '?radio_status_nenul=all'\
                    '&filter_location=3' \
                    '&field_location='\
                    '&filter_code=3'\
                    '&field_code='\
                    '&filter_contract=3'\
                    '&field_contract='\
                    '&filter_phone=2'\
                    '&field_phone='\
                    '&filter_notes=3'\
                    '&field_notes='\
                    '&filter_status_retea=3'\
                    '&field_status_retea='\
                    '&filter_package=3'\
                    '&field_package='\
                    '&filter_odf_port=3'\
                    '&field_odf_port='\
                    '&filter_pon=3'\
                    '&field_pon='\
                    '&filter_mac=3'\
                    '&field_mac='\
                    f'&field_onu_mac={mac_onu}'\
                    '&filter_ip=3'\
                    '&field_ip='\
                    '&filter_status_onu=3'\
                    '&field_status_onu='
                    ).text
                    soup = BeautifulSoup(source, 'lxml')        

                    contract = soup.find_all(class_="contract-number")

                    for client in contract:
                        if client.text != 'None':
                            return client.text
                except AttributeError as e:
                    print(f"""clientul cu Mac ONU : {mac_onu} nu a
                            fost gasit in ERP (asta inseamna ca o sa 
                            il cauti de mana in Fiber/ERP si ii faci deranjament 
                            sau daca nu il gasesti il anunti pe Dan!"""
                        )
                    return 'Nu am gasit contractul in ERP'


        # Functia primeste mac ONU din tabel si returneaza numarul de contract din ERP
        def get_contract(mac_onu, s):
            try:
                
                source = s.get('https://erp.jcs.jo/apartments/manage/' \
                    '?radio_status_nenul=all'\
                    '&filter_location=3' \
                    '&field_location='\
                    '&filter_code=3'\
                    '&field_code='\
                    '&filter_contract=3'\
                    '&field_contract='\
                    '&filter_phone=2'\
                    '&field_phone='\
                    '&filter_notes=3'\
                    '&field_notes='\
                    '&filter_status_retea=3'\
                    '&field_status_retea='\
                    '&filter_package=3'\
                    '&field_package='\
                    '&filter_odf_port=3'\
                    '&field_odf_port='\
                    '&filter_pon=3'\
                    '&field_pon='\
                    '&filter_mac=3'\
                    '&field_mac='\
                    f'&field_onu_mac={mac_onu}'\
                    '&filter_ip=3'\
                    '&field_ip='\
                    '&filter_status_onu=3'\
                    '&field_status_onu='
                    ).text
                soup = BeautifulSoup(source, 'lxml')        

                contract = soup.find_all(class_="contract-number")

                for client in contract:
                    if client.text != 'None':
                        return client.text
            except AttributeError as e:
                print(f'clientul cu Mac ONU : {mac_onu} nu a fost gasit in ERP (asta inseamna ca o sa il cauti de mana in Fiber/ERP si ii faci deranjament sau daca nu il gasesti il anunti pe Dan!')
                return 'Nu am gasit contractul in ERP'



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