from bs4 import BeautifulSoup



# In clasa erp gasim toate functiile care preiau date din ERP
class erp:
        def __init__(self, mac_onu, session):
            self.mac_onu = mac_onu
            self.session = session

        # Returneaza linia de tabel cu datele clientului din ERP printr-o lista
        def get_client_data(self):
            try:
                
                source = self.session.get('https://erp.jcs.jo/apartments/manage/?'\
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
                f'&field_onu_mac={self.mac_onu}'\
                '&filter_ip=3'\
                '&field_ip='\
                '&filter_status_onu=3'\
                '&field_status_onu='
                ).text

                soup = BeautifulSoup(source, 'lxml')        

                tabel = soup.find('tbody')
                for raw in tabel.find_all('tr'):
                    client_data = raw.find_all('td')
                    if(client_data[7].text != 'None'):
                        return client_data
                

            except AttributeError as e:
                print(f'Clientul cu Mac ONU : {self.mac_onu} nu a'\
                       'fost gasit in ERP '
                     )
                print(e)

            return "N-a gasit locatia"
        
        def get_contract(self):
            try:
                data = self.get_client_data()[4]
                return data.find('span').text
            except AttributeError as e:
                print(f'clientul cu Mac ONU : {self.mac_onu} nu a fost gasit in ERP (asta inseamna ca o sa il cauti de mana in Fiber/ERP si ii faci deranjament sau daca nu il gasesti il anunti pe Dan!')
                return 'Nu am gasit contractul in ERP'

        def get_location(self):
            try:
                return self.get_client_data()[2].text
            except AttributeError as e:
                print(f'clientul cu Mac ONU : {self.mac_onu} nu a fost gasit in ERP (asta inseamna ca o sa il cauti de mana in Fiber/ERP si ii faci deranjament sau daca nu il gasesti il anunti pe Dan!')
                
        def get_pon(self):
            try:
                return self.get_client_data()[10].text
            except AttributeError as e:
                print(f'clientul cu Mac ONU : {self.mac_onu} nu a fost gasit in ERP (asta inseamna ca o sa il cauti de mana in Fiber/ERP si ii faci deranjament sau daca nu il gasesti il anunti pe Dan!')
                

        def get_neighours_mac_onu(self, location):
            try:
                vecini = []
                source = self.session.get('https://erp.jcs.jo/apartments/manage/' \
                                          '?radio_status_nenul=yes' \
                                           '&filter_location=3' \
                                           f'&field_location={location}'
                ).text

                soup = BeautifulSoup(source, 'lxml')        

                tabel = soup.find('tbody')
                for raw in tabel.find_all('tr'):
                    client_data = raw.find_all('td')
                    if(client_data[7].text != 'None'):
                        vecini.append(client_data[7].text[6:].lower())
                
                return vecini
            except AttributeError as e:
                print(f'Clientul cu Mac ONU : {self.mac_onu} nu a'\
                       'fost gasit in ERP '
                     )
                print(e)