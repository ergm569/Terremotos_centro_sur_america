# -*- coding: utf-8 -*-
import requests

#Petición a la web. Peru 2010
page = requests.get('https://www.volcanodiscovery.com/es/earthquakes/peru/archive/2010.html')
#page.status_code
#page.content

#Obtención y 'Parse' de la página web
from bs4 import BeautifulSoup.find_all
soup = BeautifulSoup(page.content)
print(soup.prettify)

#Obtener la tabla con terremotos
tabla = soup.find(id="qTable")


#Pruebas de extracción
tabla.find_all('tr')
tabla.find_all(class="q4")
tabla.find_all(id="quake-323075")

#Extración método 1
import re
for tag in tabla.find_all(id = re.compile("quake")):
    print(tag.name)

#Extración método 2
tabla.find_all(id = re.compile("^quake-"))