#!/usr/bin/python
import subprocess
import sys
from lxml import etree





#Funcion que automatiza la creacion de ficheros .qcow2 y XML
def crear():
   	# Se copia el archivo
    subprocess.call("sudo cp plantilla-vm-p3.xml prueba1.xml", shell=True)
    subprocess.call("sudo chmod 777 prueba1.xml", shell=True)
   	# Falta copiar VM

    # Abre el archivo XML copiado
    plantilla = etree.parse('prueba1.xml')

    #Localiza la etiqueta a modificar
    source = plantilla.find('devices/disk/source')#.attrib

    print (source)
    #source['file'] = "prueba1.qcow2"


crear()


#def arrancar():
    #Arranca las VMs y mostrar las consolas correspondientes

#def parar():
    #Para las VMs

#def destruir():
    #Libera el escenario y borra todos los ficheros generados

