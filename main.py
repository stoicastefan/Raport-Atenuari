from selenium import webdriver


PATH = "/home/stefan/Documents/chromedriver"
driver = webdriver.Chrome(PATH)

driver.get("http://monitor.jcs.jo/onu/activated_onu.php")

driver.implicitly_wait(3)


body = driver.find_element_by_tag_name('tbody')

file_data = []

body_rows = driver.find_elements_by_tag_name('tr')


file_data.append('{| class="wikitable collapsible sortable"'.encode('utf8'))
data = body_rows[0].find_elements_by_tag_name('td')
file_row=[]
file_row.append("! ".encode('utf8'))
for datum in data:
    datum_text = datum.text.encode('utf8')
    file_row.append(datum_text)
    file_row.append("  || ".encode('utf8'))
file_data.append(b''.join(file_row[:-1]))
file_data.append("|- ".encode('utf8'))

index=0
for row in body_rows[1:]:
    index +=1
    print(index)
    if index == 10:
        break
    data = row.find_elements_by_tag_name('td')
    file_row=[]
    file_row.append("| ".encode('utf8'))
    for datum in data:        
        datum_text = datum.text.encode('utf8')
        file_row.append(datum_text)
        file_row.append("  || ".encode('utf8'))
    file_data.append(b''.join(file_row[:-1]))
    file_data.append("|- ".encode('utf8'))
file_data[-1] = "|} ".encode('utf8')
with open('srcFile' , "wb") as f:
    f.write(b"\n".join(file_data))




