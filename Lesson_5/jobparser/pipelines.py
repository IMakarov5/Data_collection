# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re


class JobparserPipeline:
    def __init__ (self):
        client = MongoClient('localhost', 27117)
        self.mongo_base = client.vacancies

    
    def process_item(self, item, spider):
        if item.get('salary'):

            if (item.get('salary')[0] == 'от '):
                item['min_salary'] = int (re.sub("[^0123456789\.]","",(item.get('salary')[1]) ))
            elif (item.get('salary')[0] == 'до '):
                item['max_salary'] = int (re.sub("[^0123456789\.]","",(item.get('salary')[1]) ))
            
            if (item.get('salary')[2]==' до '):
                item['max_salary'] = int (re.sub("[^0123456789\.]","",(item.get('salary')[3]) ))
                item['tax_salary'] = item.get('salary')[7]
            if (item.get('salary')[3]=='₽'):
                item['сur_salary'] = 'Рубли'
                item['tax_salary'] = item.get('salary')[5]
            elif (item.get('salary')[5]=='₽'):
                item['сur_salary'] = 'Рубли'

            
            
        # else:
        #     item['min_salary'] = 0
        # #    item['max_salary'] = int (item.get('salary')[3])
        
        
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item
