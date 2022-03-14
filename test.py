from encodings import utf_8
import requests
from bs4 import BeautifulSoup
import json

f = open("AllactivatedONUs.html", "r")
source = f.read()

soup = BeautifulSoup(source , 'lxml')

open("srcFile", "w").close()
f = open("srcFile", "a")

linkLoss=[]
highAtt = []

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
    status = int(raw.find_all('td')[6].text)
    recive = float(raw.find_all('td')[9].text)
    print(recive)
    if recive < -30 :
        highAtt.append(raw.find_all('td')[7].text)
    if status == 0 or status == 4 :
        linkLoss.append(raw.find_all('td')[7].text)
print('Link loss este:')
print(linkLoss)        
print('High att este:')
print(highAtt)    

bodyPage = soup.body
bodyPage.table.decompose()
stats=bodyPage.text.strip()
stats = stats.split('\n')
stats='\n|-\n| '.join(stats)

f.write(f'\n|-\n| {stats}')

f.write('\n|}')
f.close()

#primeste mac onu din tabel si returneaza numarul de contract din erp
def getContract(macOnu, s):
    print(f'https://erp.jcs.jo/apartments/manage/?radio_status_nenul=all&filter_location=3&field_location=&filter_code=3&field_code=&filter_contract=3&field_contract=&filter_phone=2&field_phone=&filter_notes=3&field_notes=&filter_status_retea=3&field_status_retea=&filter_package=3&field_package=&filter_odf_port=3&field_odf_port=&filter_pon=3&field_pon=&filter_mac=3&field_mac=&filter_onu_mac=3&field_onu_mac={macOnu}&filter_ip=3&field_ip=&filter_status_onu=3&field_status_onu=')
    source = s.get(f'https://erp.jcs.jo/apartments/manage/?radio_status_nenul=all&filter_location=3&field_location=&filter_code=3&field_code=&filter_contract=3&field_contract=&filter_phone=2&field_phone=&filter_notes=3&field_notes=&filter_status_retea=3&field_status_retea=&filter_package=3&field_package=&filter_odf_port=3&field_odf_port=&filter_pon=3&field_pon=&filter_mac=3&field_mac=&filter_onu_mac=3&field_onu_mac={macOnu}&filter_ip=3&field_ip=&filter_status_onu=3&field_status_onu=').text
    print(source)
    soup = BeautifulSoup(source, 'lxml')
    contract = soup.find("span")
    return contract

def login(name, password):
    s = requests.Session()
    
    site = s.get("https://erp.jcs.jo/login/")
    bs_content = BeautifulSoup(site.content, "html.parser")
    token = bs_content.find("input",{"name":"csrfmiddlewaretoken"})["value"]
    print(token)
    payload = {
    'csrfmiddlewaretoken' : token,
    'username' : name,
    'password' : password 
    }
    res = s.post('https://erp.jcs.jo/login/', payload)
    print(res.text)
    print(payload)
   
    #s.headers.update({'csrftoken' : json.loads(res.content)['csrfmiddlewaretoken']})


session = login('stefan', 'stefan112')
print(session)