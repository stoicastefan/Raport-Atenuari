import requests
from bs4 import BeautifulSoup

source = requests.get('http://monitor.jcs.jo/onu/activated_onu.php').text

soup = BeautifulSoup(source, 'lxml')
open("srcFile", "w").close()
f = open("srcFile", "a")

f.write('{| class="wikitable collapsible sortable"\n')
raw = soup.find('tr')
f.write(f'! {raw.find("td").text} ')
for el in raw.find_all('td')[1::]:
        f.write(f'  || {el.text}')
for raw in soup.find_all('tr')[1::]:
    f.write(f'\n|-\n| {raw.find("td").text} ')
    for el in raw.find_all('td')[1::]:
        f.write(f'  || {el.text}')

f.write('\n|}')
f.close()