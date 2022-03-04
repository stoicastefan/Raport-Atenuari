from selenium import webdriver


PATH = "/home/stefan/Documents/chromedriver"
driver = webdriver.Chrome(PATH)

driver.get("http://monitor.jcs.jo/onu/activated_onu.php")

driver.implicitly_wait(3)


body = driver.find_element_by_tag_name('tbody')

file_data = []

body_rows = driver.find_elements_by_tag_name('tr')


file_data.append('{| class="wikitable collapsible sortable"')
data = body_rows[0].find_elements_by_tag_name('td')
file_row=[]
file_row.append("! ")
for datum in data:
    datum_text = datum.text
    file_row.append(datum_text)
    file_row.append("  || ")
file_data.append(''.join(file_row[:-1]))
file_data.append("|- ")

index=0
for row in body_rows[1:]:
    index +=1
    print(index)
    
    data = row.find_elements_by_tag_name('td')

    file_row2 ='  || '.join(list(map(data,lambda x: x.txt)))
    file_data.append('| ' + file_row2)
    file_data.append("|- ")
file_data[-1] = "|} "
with open('srcFile' , "w") as f:
    f.write("\n".join(file_data))


