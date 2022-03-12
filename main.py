import requests
from bs4 import BeautifulSoup

source = requests.get('http://monitor.jcs.jo/onu/activated_onu.php').text

soup = BeautifulSoup(source, 'lxml')
open("srcFile", "w").close()
f = open("srcFile", "a")
linkLoss  = []
highAtt = []
f.write('{| class="wikitable collapsible sortable"\n')
raw = soup.find('tr')
f.write(f'! {raw.find("td").text} ')
for el in raw.find_all('td')[1::]:
        f.write(f'  || {el.text}')
for raw in soup.find_all('tr')[1::]:
    f.write(f'\n|-\n| {raw.find("td").text} ')
    for el in raw.find_all('td')[1::]:
        f.write(f'  || {el.text}')
    status = int(raw.find_all('td')[6].text)
    recive = float(raw.find_all('td')[8].text)
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