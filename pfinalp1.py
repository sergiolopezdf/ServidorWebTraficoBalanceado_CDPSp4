#!/usr/bin/python
import subprocess
import sys
from lxml import etree
import copy





#Funcion que automatiza la creacion de ficheros .qcow2 y XML
def crear():
   	# Se copia el archivo
    #subprocess.call("sudo cp plantilla-vm-p3.xml prueba1.xml", shell=True)
    #subprocess.call("sudo chmod 777 prueba1.xml", shell=True)
   	# Falta copiar VM

    # Creamos los clientes
    generateNewVM("c1", "LAN1")

    # Creamos los servidores. Habra que modificarlo para admitirlo como parametro
    generateNewVM("s1", "LAN2")
    generateNewVM("s2", "LAN2")
    generateNewVM("s3", "LAN2")

    # Creamos LB
    generateLB()

def generateNewVM(name, LAN):
    # Abre el archivo XML copiado
    plantilla = etree.parse('plantilla-vm-p3.xml')

    # Selecciona la imagen a usar
    sourceFile = plantilla.find('devices/disk/source')
    sourceFile.set("file", ""+name+".qcow2")

    # Cambia el nombre de la VM
    vmName = plantilla.find('name')
    vmName.text = name

    # Anade la VM a la subred correspondiente
    sourceBridge = plantilla.find('devices/interface/source')
    sourceBridge.set("bridge", LAN) 

    # Exportamos a un nuevo archivo 
    plantilla.write(open(''+name+'.xml', 'w'), encoding='UTF-8')

    # Damos permiso de escritura
    subprocess.call("sudo chmod 777 "+name+".xml", shell=True)

    # Copiamos la imagen de la VM correspondiente
    # subprocess.call("sudo cp cdps-vm-base-p3.qcow2 "+name+".xml", shell=True)

def generateLB():
   # Abre el archivo XML copiado
    plantilla = etree.parse('plantilla-vm-p3.xml')

    # Selecciona la imagen a usar
    sourceFile = plantilla.find('devices/disk/source')
    sourceFile.set("file", "lb.qcow2")

    # Cambia el nombre de la VM
    vmName = plantilla.find('name')
    vmName.text = "lb"

    # Anade la VM a la subred correspondiente
    sourceBridge = plantilla.find('devices/interface')
        
    interface1 = sourceBridge
    interface2 = copy.deepcopy(sourceBridge)


    interface1.find('source').set("bridge", "LAN1") 
    interface2.find('source').set("bridge", "LAN2") 



    
    plantilla.find('devices').append(interface1)
    plantilla.find('devices').append(interface2)

    # Exportamos a un nuevo archivo 
    plantilla.write(open('lb.xml', 'w'), encoding='UTF-8')

    # Damos permiso de escritura
    subprocess.call("sudo chmod 777 lb.xml", shell=True)

    # Copiamos la imagen de la VM correspondiente
    # subprocess.call("sudo cp cdps-vm-base-p3.qcow2 "+name+".xml", shell=True)


#def arrancar():
    #Arranca las VMs y mostrar las consolas correspondientes

#def parar():
    #Para las VMs

#def destruir():
    #Libera el escenario y borra todos los ficheros generados

crear()