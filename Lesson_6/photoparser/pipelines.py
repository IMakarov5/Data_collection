# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy

from itemadapter import ItemAdapter

from scrapy.pipelines.images import ImagesPipeline
from pprint import pprint

import json


class PhotoparserPipeline:
    def process_item(self, item, spider):
       
        separator = ' ; '

        items={}
        
        items['name'] = item['name']
        items['photos']= item['photos']
        items['url']=item['url']
        items['category']=item['category']
        # сохранение данных в JSON-файл
        with open('photos/photos_file.json', 'a', encoding='utf-8') as file:
             json.dump(items, file)
       
        with open('photos/photos_file.csv', 'a', encoding='utf-8') as file:
             file.write(item['name']+ separator 
                        + item['photos'][0]['path'] + separator
                        + item['photos'][0]['url'] + separator 
                        + ', '.join(map(str, item['category']))
                        )
            
             file.write('\n')
        
        return item

class PhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
          if item['photos']:
            for img_url in item['photos']:
                try:
                    yield scrapy.Request(img_url)
                except Exception as e:
                    print(e)
        

    def item_completed(self, results, item, info):
       
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
                   
        return item