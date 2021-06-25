import base64
from time import sleep

import requests

# print(password, "    ", len(password))
password = 'JeSuisContent!'
password = password.encode('utf-8')
password = base64.b64encode(password)
list = ["Lionel-Richie-lionelrichie@gmail.com",
        "Simone-DeBeauvoir-simone.de.beauvoir@closer.mag",
        "Michael-Apeupres-jesaisplus@perdu.fr"]
for name in list:
    sleep(1)
    prenom = name.split("-")[0]
    nom = name.split("-")[1]
    mail = name.split("-")[2]
    r = requests.post('http://127.0.0.1:5000/login', data={'email': mail, 'password': password})
    print(r.content)
    r = requests.get('http://127.0.0.1:5000/logout')
    print(r.content)
