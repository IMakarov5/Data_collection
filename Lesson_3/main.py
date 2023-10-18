import requests
import json
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from sshtunnel import SSHTunnelForwarder
from pprint import pprint

# читаем фалй конфигурации
config_path = 'config.env'
if os.path.exists(config_path):
    load_dotenv(config_path)



# создание SSH тунеля, так как MongoDB на удаленном сервере и там открыт только порт SSH
server = SSHTunnelForwarder(
    os.getenv("MONGO_HOST"),
    ssh_username=os.getenv("MONGO_USER"),
    ssh_password=os.getenv("MONGO_PASS"),
    remote_bind_address=('127.0.0.1', 27017)
)

# подключение к Mongo через тунель
server.start()
client = MongoClient('127.0.0.1', server.local_bind_port) # server.local_bind_port is assigned local port

# Выбор базы данных и коллекции
db = client['shop']
books = db['books']

# очистка базы
books.delete_many({})

# Чтение файла JSON
with open('books_toscrape.json', 'r') as file:
    data = json.load(file)

count_duplicated = 0

for book in data:   
    # print (book['Book name'][1][36:-11])
    _id = book['Book name'][1][36:-11]
    book["_id"] = _id
    try:
        books.insert_one(book)
    except:
        count_duplicated += 1
        print(books)

# Получение количества документов в коллекции с помощью функции count_documents()
count = books.count_documents({})
print(f'Число записей в базе данных: {count}')

# найти все документы в коллекции "books" и вывести их на консоль
for a in db.books.find():
    print (a)

# Вывести книге, где в price £5 
print("Вывести книге, где в price £5 ")
query = {"price" : {'$regex' : '£5.'}}
for doc in db.books.find (query):
    print (doc)
print(f"Количество книг, где в price £5: {books.count_documents(query)}")


# вывести книге, где остатков более 19 $gte (больше или равно)
print("Вывести книге, где остатков более 19: ")
query = {"stock" : {'$gte' : 19}}
for doc in db.books.find (query):
    print (doc)
print(f"Количество книг, где остатков более 19: {books.count_documents(query)}")

# вывести книге, где количество менее 5 $lte (меньше или равно)
print("Вывести книге, где остатков менее 5: ")
query = {"stock" : {'$lte' : 5}}
for doc in db.books.find (query):
    print (doc)
print(f"Количество книг, где остатков менее 5: {books.count_documents(query)}")


server.stop()