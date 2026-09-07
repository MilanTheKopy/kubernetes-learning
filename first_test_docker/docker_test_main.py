import numpy as np
import socket
with socket.create_server(("", 50000)) as s: #IP Adresse leer: alle adressen genutzt, ports ab 50.000 können safe genutzt werden
    s.listen(1) #1 ist die anzahl der zu puffernden Verbindungsversuche clientseitig
    while True:
        conn, addr = s.accept() #mit verbindung eines clients kann diese verbindung und die clientadresse nun genutzt werden
        while data := conn.recv(32): #Die schleife wird für jede msg des clients durchlaufen, bis diese leer ist, was einen verbindungsabbruch bedeutet
            print(f"{addr[0]}: {data.decode()}") 
            response = input("Antwort: ") #die schleife wartet jeweils auf antwort des servers
            conn.send(response.encode()) #und sendet diese
        conn.close() #nach abbruch der verbindung clientseitig wird diese geschlossen