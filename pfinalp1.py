#!/usr/bin/python
import subprocess
import sys
from lxml import etree





#Funcion que automatiza la creacion de ficheros .qcow2 y XML
def crear():
   	# Se copia el archivo
    #subprocess.call("sudo cp plantilla-vm-p3.xml prueba1.xml", shell=True)
    #subprocess.call("sudo chmod 777 prueba1.xml", shell=True)
   	# Falta copiar VM

    # Abre el archivo XML copiado
    plantilla = etree.parse('plantilla-vm-p3.xml')

    #Localiza las etiqueta a modificar
    sourceFile = plantilla.find('devices/disk/source')
    sourceFile.set("file", "prueba1.qcow2")

    name = plantilla.find('name')
    name.text = "VM1"

    sourceBridge = plantilla.find('devices/interface/source')
    sourceBridge.set("bridge", "LAN1") # O LAN2

    # Exportamos a un nuevo archivo 
    plantilla.write(open('plantilla1.xml', 'w'), encoding='UTF-8')


crear()


#def arrancar():
    #Arranca las VMs y mostrar las consolas correspondientes

#def parar():
    #Para las VMs

#def destruir():
    #Libera el escenario y borra todos los ficheros generados

