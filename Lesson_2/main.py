import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pprint import pprint
import time
import json

ua = UserAgent()
#print(ua.chrome)



url = "http://books.toscrape.com/"

headers = {"User-Agent": ua.chrome} 
# params = {"ref_": "bo_nb_hm_tab"}

books=[]

n=1
while n<51:
    response = requests.get(url+"catalogue/page-"+str(n)+".html", headers=headers)
    # print(response.status_code)
    # print(response.text)
    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find_all('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'})
    print(f"В работе {n} страница, количество книжек на странице: {len(rows)}")
    
    for row in rows:
        book = {}
        #film['realeses'] = row.find('td', {'class':'mojo-field-type-positive_integer'}).getText()
        # print(row)
        # print('строка ', n)
        name_info = row.find('h3').findChildren()[0]
        book['Book name'] = [name_info.get('title'), url + 'catalogue/' + name_info.get('href')]
        try:
            book['price'] = row.find('p',{'class':'price_color'}).getText()[1:]
        except:
            book['price'] = None

        response = requests.get(url + 'catalogue/' + name_info.get('href'), headers=headers)
        # print(respons)
        soup = BeautifulSoup(response.content, 'html.parser')
        book['stock'] = int(soup.find('p',{'class':'instock availability'}).getText()[25:27])
        try:
            book['description'] = soup.find('p',{'class':''}).getText().replace("’", "")
        except:
            book['description'] = None

        books.append(book)
        # time.sleep(10)
    
    n=n+1

# pprint(books)
pprint(len(books))

# сохранение данных в JSON-файл
with open('books_toscrape.json', 'w', encoding='utf-8') as file:
    json.dump(books, file, ensure_ascii=False)

  