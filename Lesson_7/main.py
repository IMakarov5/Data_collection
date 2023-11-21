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

s_url = 'https://www.huntworld.ru'

driver.get("https://www.huntworld.ru/catalog/okhota_i_sportivnaya_strelba/okhotniche_oruzhie/gladkostvolnye_ruzhya/?ysclid=lp4f6951c2715525594&PAGEN_1=1")
# n=1

# time.sleep(20)
#while True:

while True:
    # driver.get("https://www.huntworld.ru/catalog/okhota_i_sportivnaya_strelba/okhotniche_oruzhie/gladkostvolnye_ruzhya/?ysclid=lgru9sgwb526984936&PAGEN_1="+str(n))
    wait = WebDriverWait(driver, 120)
    guns = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="card-container"]')))

    print(len(guns))
    count = len(guns)
    # driver.execute_script("window.scrollBy(0,3000)")
    
    try:
        button = driver.find_element(By.XPATH, '//a[@class="long-grey-button js-load-more"]')
        
        actions = ActionChains(driver)
        actions.move_to_element(button).click() 
        actions.perform()
        time.sleep(12)
        # guns = driver.find_elements(By.XPATH, '//div[@class="card-container"]')
        # if len(guns) == count: #vor len(guns) > 45
        #     break
    except:
        break

items_lists = []

for gun in guns:
        items_list = {}
        items_list ['id'] = gun.find_element(By.XPATH, '//div[@class="card-container"]//a[@class="product-preview__pictures picture-slider js-preview-slider"]').get_attribute('data-id')
        items_list ['name'] = gun.find_element(By.XPATH, './/a[@class="product-preview__name no-link"]').text
        items_list ['price'] = gun.find_element(By.XPATH, './/div[@class="product-preview__prices"]').text
        items_list ['url'] = gun.find_element(By.XPATH, './/a[@class="product-preview__name no-link"]').get_attribute('href')
        
        items_lists.append(items_list)

# pprint(items_lists)
# сохранение данных в JSON-файл
with open('./photo/info_items.json', 'w', encoding='utf-8') as file:
    json.dump(items_lists, file, ensure_ascii=False)

items_lists_full=[]
for item in items_lists:
        
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
                
                photo_list['photo_name'] = 'photo/' + photo_name
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









