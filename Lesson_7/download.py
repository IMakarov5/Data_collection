from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pprint import pprint
import requests
import json
import time




options = Options()
options.add_argument('start-maximized')

driver = webdriver.Chrome(options=options)



# чтение из JSON-файл
with open('./photo/info_items.json', 'r') as j:
    items_lists = json.load(j)

# # чтение из JSON-файл
with open('./photo/info_items_full.json', 'r') as jd:
    items_lists_dow = json.load(jd)

zr = [ x['url'] for x in items_lists_dow]

items_lists_full=[]
for item in items_lists:
        if item['url'] not in zr:
        #print(item['url'])
            photo_lists=[]
            driver.get(item['url'])
            wait = WebDriverWait(driver, 60)
            photo_gun = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="product-detail__pictures pic-block"]')))
            while True:
                photo_list={}
                try:
                    button = driver.find_element(By.XPATH, '//div[@class="product-detail__pictures pic-block"]//div[@class="arrow next"]')
                    # print(button)
                    actions = ActionChains(driver)
                    actions.move_to_element(button).click()
                    actions.perform()


                    photo_url = driver.find_element(By.XPATH, '//div[@class="swiper-slide swiper-slide-active"]/a[@data-fancybox="item-view"]').get_attribute('href')
                    photo_name = '/'.join(photo_url.split('/')[-1:])
                    
                    photo_list['photo_name'] = photo_name
                    photo_list['photo_url'] = photo_url

                    
                    response = requests.get(photo_url)
                    time.sleep(6)
                    with open(f'./photo/{photo_name}','wb') as f:
                            f.write(response.content)
                            
                    photo_lists.append(photo_list)
                except:
                    break
            
            
            item['photo'] = photo_lists
            items_lists_full.append(item)

            # сохранение данных в JSON-файл
            with open('./photo/info_items_full.json', 'w', encoding='utf-8') as file:
                json.dump(items_lists_full, file, ensure_ascii=False)






driver.close()
