from bs4 import BeautifulSoup



# In clasa erp gasim toate functiile care preiau date din ERP
class erp:

        def get_locatie(mac_onu, s):
            try:
                
                source = s.get('https://erp.jcs.jo/apartments/manage/?'\
                'radio_status_nenul=all'\
                '&filter_location=3'\
                '&field_location=&'\
                'filter_code=3'\
                '&field_code='\
                '&filter_contract=3'\
                '&field_contract=&'\
                'filter_phone=2'\
                '&field_phone='\
                '&filter_notes=3'\
                '&field_notes='\
                '&filter_status_retea=3'\
                '&field_status_retea='\
                '&filter_package=3'\
                '&field_package=&'\
                'filter_odf_port=3'\
                '&field_odf_port='\
                '&filter_pon=3'\
                '&field_pon='\
                '&filter_mac=3'\
                '&field_mac=&'\
                'filter_onu_mac=3'\
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
                    if(test[7].text != 'None'):
                        return test[2].text
                

            except AttributeError as e:
                print(f'Locatia clientului cu Mac ONU : {mac_onu} nu a'\
                       'fost gasita in ERP '
                     )
                print(e)
            return "nu s-a gasit locatia"


        # Functia primeste mac ONU din tabel si returneaza numarul de contract din ERP

        
        def get_contract(mac_onu, s):
            try:
                
                source = s.get('https://erp.jcs.jo/apartments/manage/?'\
                'radio_status_nenul=all'\
                '&filter_location=3'\
                '&field_location=&'\
                'filter_code=3'\
                '&field_code='\
                '&filter_contract=3'\
                '&field_contract=&'\
                'filter_phone=2'\
                '&field_phone='\
                '&filter_notes=3'\
                '&field_notes='\
                '&filter_status_retea=3'\
                '&field_status_retea='\
                '&filter_package=3'\
                '&field_package=&'\
                'filter_odf_port=3'\
                '&field_odf_port='\
                '&filter_pon=3'\
                '&field_pon='\
                '&filter_mac=3'\
                '&field_mac=&'\
                'filter_onu_mac=3'\
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


