import base64
from time import sleep

import requests
import string
import random
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
    r = requests.post('http://127.0.0.1:5000/register',
                      data={'email': mail, 'password': password, 'nom': nom, 'prenom': prenom})
    print(r.content)
