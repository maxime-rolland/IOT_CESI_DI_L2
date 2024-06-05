# FONCTION PRINCIPALE main.py, lancée automatiquement au boot du rpy

# Import des lib externes
import time
import BME280

from machine import Pin, I2C
# Import des fonctions 
from do_connect import *
from do_request import *
from do_light import *

print("Hello")
# On se connecte au réseau
networkInfos=do_connect()

# On construit l'url en indiquant l'adresse mac de la machine 
# récupérée lors de la connexion au réseau
getUrl="https://backend.groupe3.learn-it.ovh/leds?mac="+networkInfos['mac']
postUrl="https://backend.groupe3.learn-it.ovh/raspberry/"+networkInfos['mac']+"/envInfos"
i2c = I2C(id=0, scl=Pin(9), sda=Pin(8), freq=10000)
while True:
    try:
        # Initialize BME280 sensor
        bme = BME280.BME280(i2c=i2c)
        
        # Read sensor data
        #Exprimé en degré Celcius
        tempC = bme.temperature
        #Exprimé en %
        hum = bme.humidity
        # Exprimé en hPA
        pres = bme.pressure
        
        data={
            'temperature':tempC,
            'humidity':hum,
            'pression':pres
            }
        print(data)
        #On envoie le POST avec les infos sur l'environnement
        do_post(postUrl,data)
        print('debug')
        # On récupère le JSON en faisant une requete à l'url construite
        json=do_get(getUrl)
        # Pour chaque LED de notre JSON (array)
        for led in json:
            value=0
            # Si l'état est à true, on passe value à 1
            if led['etat']:
                value=1
            # On passe la value à la fonction chargée d'allumer / éteindre les LEDs
            do_light(led['label'], value)
        #On attend 2 secondes avant de recommencer    
        time.sleep(1)
    except:
        print ("erreur")
        time.sleep(5)

