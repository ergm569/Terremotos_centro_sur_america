# Importando todas las librerias necesarias

import requests
import numpy as np
import pandas as pnds
from bs4 import BeautifulSoup, NavigableString, Comment
import bs4
import time
from urllib.request import Request, urlopen


def webScrapingTerremoto(año = 2010,pais = 'peru'):
    
    #Asignar página web
    url ='https://www.volcanodiscovery.com/es/earthquakes/'
    archive = '/archive/'
    html = '.html'
    cabecera = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url+pais+archive+str(año)+html,headers=cabecera)
    #page = requests.get(url+pais+archive+str(año)+html)
    page = urlopen(req)
    #Inicializar tiempo de respuesta
    t0 = time.time()
    
    #Obtención y 'Parse' de la página web
    soup = BeautifulSoup(page, 'html.parser')
    tabla = soup.find(id="qTable")
        
    columnaFechayHora = []
    columnaMagnitud = []
    columnaProfundidad = []
    columnaUbicacion = []
        
    for filas in tabla.find_all("tr", {"class": ["q4", "q5"]}):
        contenido = filas.select_one('td:-soup-contains("GMT")').text.strip()
        if(contenido.endswith('GMT') == True):
            columnaFechayHora.append(contenido)
        for filas2 in filas.find_all("td", {"class": "mList"}):
            for filas3 in filas2.find_all("div", {"class": "magCircle mag4"}):
                columnaMagnitud.append(filas3.text)
            for filas4 in filas2.find_all("br"):
                columnaProfundidad.append(filas4.next_sibling)
        for filas5 in filas.find_all("td", {"class": "list_region"}):
            columnaUbicacion.append(filas5.get_text())
        
    tabla_final = pnds.DataFrame(list(zip(columnaFechayHora, columnaMagnitud, columnaProfundidad, columnaUbicacion)), columns = ["Fecha y Hora", "Magnitud", "Profundidad", "Ubicacion"])
        
    tabla_final['Año'] = año
    tabla_final['Pais'] = pais
        
    #print(tabla_final)
    return tabla_final

    #Estimación del tiempo de respuesta en segundos
    response_delay = time.time() - t0
    
    #Espera de 10x, con respecto al tiempo de respuesta
    time.sleep(20 * response_delay)


#Definir años y pais de extracción
año_inicio = 2010
año_final = 2021
paises = []
paises = ['dominican-republic','guatemala','costarica','mexico','panama','puertorico','argentina','bolivia','brazil','chile','colombia','ecuador','paraguay','peru','venezuela']

#Extracción
tabla_total = webScrapingTerremoto(2010,'peru')
for pais in paises:
    for año in range(año_inicio,año_final+1):
        tabla_aux = webScrapingTerremoto(año,pais)
        tabla_total = pnds.merge(tabla_total, tabla_aux, how='outer')
        print('Extracción: '+pais+' '+str(año))
    
#Exportación de csv
tabla_total.to_csv(r'.\terremotos_centro_sur_america.csv', index = False, header=True)
