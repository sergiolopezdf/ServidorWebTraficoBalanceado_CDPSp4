#!/usr/bin/python
import subprocess
import sys
from lxml import etree
import copy
import os

#Funcion que automatiza la creacion de ficheros .qcow2 y XML
def crear(nServers):
    # Creamos los clientes
    generateNewVM("c1", "LAN1")
    subprocess.call("sudo virsh define c1.xml", shell=True)

    # Creamos los servidores
    for server in range(1, nServers + 1):
        generateNewVM("s"+str(server) , "LAN2")
        subprocess.call("sudo virsh define s"+str(server)+".xml", shell=True)
   
    # Creamos LB
    generateLB()
    subprocess.call("sudo virsh define lb.xml", shell=True)

    # Lanza virt-manager
    subprocess.call("sudo virt-manager", shell=True)


def generateNewVM(name, LAN):
    # Abre el archivo XML copiado
    plantilla = etree.parse('plantilla-vm-p3.xml')

    # Selecciona la imagen a usar
    sourceFile = plantilla.find('devices/disk/source')
    currentPath = os.getcwd()
    sourceFile.set("file", ""+currentPath+"/"+name+".qcow2")

    # Cambia el nombre de la VM
    vmName = plantilla.find('name')
    vmName.text = name

    # Anade la VM a la subred correspondiente
    sourceBridge = plantilla.find('devices/interface/source')
    sourceBridge.set("bridge", LAN) 

    # Exportamos a un nuevo archivo 
    plantilla.write(open(''+name+'.xml', 'w'), encoding='UTF-8')

    # Copiamos la imagen de la VM correspondiente
    subprocess.call("sudo qemu-img create -f qcow2 -b cdps-vm-base-p3.qcow2 "+name+".qcow2", shell=True)

    # Damos permiso de escritura
    subprocess.call("sudo chmod 777 "+name+".xml", shell=True)
    subprocess.call("sudo chmod 777 "+name+".qcow2", shell=True)

def generateLB():
   # Abre el archivo XML copiado
    plantilla = etree.parse('plantilla-vm-p3.xml')

    # Selecciona la imagen a usar
    sourceFile = plantilla.find('devices/disk/source')
    currentPath = os.getcwd()
    sourceFile.set("file", ""+currentPath+"/lb.qcow2")

    # Cambia el nombre de la VM
    vmName = plantilla.find('name')
    vmName.text = "lb"

    # Anade la VM a la subred correspondiente
    interface1 = plantilla.find('devices/interface')
    interface1.find('source').set("bridge", "LAN1") 

    # Como hay 2 interfaces distintos, se duplica el elemento
    interface2 = copy.deepcopy(interface1)
    interface2.find('source').set("bridge", "LAN2") 

    # Se anade. Ojo porque queda al final. Revisar
    plantilla.find('devices').append(interface2)

    # Exportamos a un nuevo archivo 
    plantilla.write(open('lb.xml', 'w'), encoding='UTF-8')

    # Copiamos la imagen de la VM correspondiente
    subprocess.call("sudo qemu-img create -f qcow2 -b cdps-vm-base-p3.qcow2 lb.qcow2", shell=True)

    # Damos permiso de escritura
    subprocess.call("sudo chmod 777 lb.xml", shell=True)
    subprocess.call("sudo chmod 777 lb.qcow2", shell=True)


#Arranca las VMs y mostrar las consolas correspondientes
def arrancar():
    return

#Para las VMs
def parar():
    return

#Libera el escenario y borra todos los ficheros generados
def destruir():
    return

# Flujo principal de ejecucion del programa
if len(sys.argv) < 2:
    sys.stderr.write("No has introducido ninguna orden\n")
    sys.exit(-1)

# Asignamos la orden
orden = sys.argv[1]

# El numero de servidores arrancados por defecto es 2
nServers = 2

# Comprobamos si se ha especificado el numero de servidores
if len(sys.argv) == 3:
    if sys.argv[2] > 5:
        nServers = 5
    elif sys.argv[2] == 0:
        nServers = 2
    else:  
        nServers = int(sys.argv[2])

# Ejecutamos la orden
if orden == "crear":
    crear(nServers)
elif orden == "arrancar":
    arrancar()
elif orden == "parar":
    parar()
elif orden == "destruir":
    destruir()
else:
    sys.stderr.write("Introduce una orden valida\n")
