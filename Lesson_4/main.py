import requests
from lxml import html
from pprint import pprint
import json

headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}

url = 'https://news.mail.ru/'
response = requests.get(url, headers=headers)

dom = html.fromstring(response.content)


items_lists = []
items = dom.xpath("//span[contains(@class,'js-topnews__item')]/a/@href")


for item in items:
    items_list = {}
    # print(item)
    response = requests.get(item, headers=headers)
    dom_item = html.fromstring(response.content)
    items_list ['href'] = item
    items_list ['name']  = dom_item.xpath("//h1[@class='hdr__inner']/text()")
    items_list ['intro']= dom_item.xpath("//div[contains(@class,'article__intro')]/p/text()")
    items_list ['time'] = dom_item.xpath("//span[contains(@class,'js-ago')]/text()")
    items_list ['source'] = dom_item.xpath("//span[@class='note']//span[@class='link__text']/text()")
    
    
    items_lists.append(items_list)


# pprint(items_lists)

# сохранение данных в JSON-файл
with open('news_mail.json', 'w', encoding='utf-8') as file:
    json.dump(items_lists, file, ensure_ascii=False)


