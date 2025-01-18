#vamos a utilizar la libreria scapy
#libreria para python en redes de facil uso 
#documentacion https://scapy.readthedocs.io/en/latest/index.html
# $ pip install scapy

import scapy.all as scapy
import requests

def scan(ip):
        #definimos variable llamada arp_request
        #scapy.ARP sirve para preguntar... Quien tiene la IP y devuelve la IP y la MAC
        arp_request = scapy.ARP(pdst=ip)
        
        #scapy.Ether sirve para preguntar... Quien tiene la MAC y devuelve la IP 
        var_broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
        
        #Ahora combinamos las dos IP y MAC
        arp_request_broadcast = var_broadcast/arp_request
        #declaramos una lista, scapy.srp obtiene dos listas, una que contiene la de anwered o respondidos y la otra la que no, obviamente usaremos las que si respondieron
        #el timeout lo pusimos por si hay un delay y el verbose para ir quitando mensajes
        #[0] solo nos devuelve la primera lista
        lista_respondidos=scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
        
        #print(list_respondidos.summary())
        
        print("IP\t\t\tMAC Address\n---------------------------------------------------")
        
        for dispositivo in lista_respondidos:
            print(dispositivo[1].psrc+" - "+dispositivo[1].hwsrc)#Segun la documentacion scapy manda dos elementos en la lisa separadas por coma, nos interasa el segundo elemento con el indice 1
            print("---------------------------")

def scandict(ip):
        arp_request = scapy.ARP(pdst=ip)
        var_broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
        #Ahora combinamos las dos IP y MAC
        arp_request_broadcast = var_broadcast/arp_request
        lista_respondidos=scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
        
        clients_list=[]
        for item in lista_respondidos:
            #creamos nuestro diccionario iterando en la lista
            cliente_dict={"ip":item[1].psrc, "mac": item[1].hwsrc}
            #y vamos agregando a la lista cada clave valor del diccionario encontrado (ip y mac)
            clients_list.append(cliente_dict)
        return clients_list

def imprimir_resultado(resultados_list):        
        print("IP\t\t\tMAC Address\n---------------------------------------------------")
        for cliente in resultados_list:
            print(cliente["ip"]+"\t\t"+cliente["mac"])#agregamos clave valor mac e ip separados por tabuladores 2
        print("---------------------------------------------")


#Para encontrar el vendor de un fabricante solo concatenamos la mac address a la url
def obtener_vendor(mac):
    """Consulta el fabricante del dispositivo basado en la dirección MAC."""
    try:
        url = f"https://api.macvendors.com/{mac}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("company", "No encontrado")
        else:
            return "No encontrado"
    except:
        return response.content.decode()

def scanvendor(ip):
    # Solicitud ARP
    arp_request = scapy.ARP(pdst=ip)
    var_broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = var_broadcast / arp_request
    
    # Envío y recepción de paquetes
    lista_respondidos = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    
    print("IP\t\t\tMAC Address\t\t\tVendor\n---------------------------------------------------------------")
    for dispositivo in lista_respondidos:
        ip = dispositivo[1].psrc
        mac = dispositivo[1].hwsrc
        vendor = obtener_vendor(mac)
        print(f"{ip}\t{mac}\t{vendor}")
        print("---------------------------")

def scan_con_arping(ip):
    scapy.arping(ip)
    
def invalida():
        return print("Opcion no valida")


print("-------- SCANNER DE RED CON PYTHON --------------")
print("-------- Author: Roberto Carlos --------------")
print("-------- Uso para personal de IT --------------")
print("------ Con conocimientos basicos de redes---------")
mired = input("Digite su red con esta cognotacion 192.168.0.1/24   ")

    
while True:
    print("1) Listado de IP con su MAC Usando Listas")
    print("2) Listado de IP con su MAC Usando diccionarios")
    #esta opcion solo la agregue pero no me sirvio porque practicamente lo hace todo y la intencion es aprender
    print("3) Listado de Dispositivos usando ArPing")
    print("4) Listado de Dispositivos Con Vendor MAC")
    print("5) Para salir")
  
    opcion=int(input("Escoja de 1) a 4) .. o 5) para salir!! ----->    "))
    if opcion == 1:
        scan(mired)
    elif opcion == 2:
        scan_resultado=scandict(mired)
        imprimir_resultado(scan_resultado)
        continue
    elif opcion == 3:
        scan_con_arping(mired)
    elif opcion == 5:
        print("Adios!!")
        break
    elif opcion == 4:
        scanvendor(mired)

    else: 
        invalida() 