import tkinter
from tkinter import *
import socket
import threading
import time
import sqlite3


def serverNit():
    while True:
        global suma
        conn, addr=s.accept()
        print("Konektovan:", addr)
        zahtev_klijenta=conn.recv(1024).decode()
        odgovor_klijentu=""

        try:
            konekcija_baza = sqlite3.connect("baza01.db")
            kursor=konekcija_baza.cursor()

            if zahtev_klijenta.find("SELECT"):
                #nije select -1
                kursor.execute(zahtev_klijenta)
                konekcija_baza.commit()
                odgovor_klijentu="Broj izmenjenih redova: "+str(konekcija_baza.total_changes)
            else:
                #jeste 0
                redovi=kursor.execute(zahtev_klijenta).fetchall()
                if len(redovi)==0:
                    odgovor_klijentu="Automobliz za trazeni kriterijum nije pronadjen!"
                else:
                    for red in redovi:
                        odgovor_klijentu+="id: "+str(red[0])+" naziv: "+red[1]+" cena: "+str(red[2])+"; "



            konekcija_baza.close()
        except Exception as e:
            odgovor_klijentu=str(e)

# #Modifikacija prilikom odbrane projekta:
#
# #Izmena
#         argumenti=zahtev_klijenta.split()
#         print(argumenti)
#         if argumenti[1] in dictDonacije.keys():
#             print("Vec je donirao")
#             dictDonacije[argumenti[1]]=int(dictDonacije[argumenti[1]])+int(argumenti[2])
#             print(dictDonacije)
#
#         else:
#             print("Prvi put donira, dodaj na listu")
#             dictDonacije[argumenti[1]]=argumenti[2]
#             print(dictDonacije)
#         suma += int(argumenti[2])
#         print(suma)
#         clanovi=""
#         for kljuc, vrednost in dictDonacije.items():
#             clanovi+=kljuc+": "+str(vrednost)+" "
#
#         odgovor_klijentu="Ukupno: "+str(suma)+" "+ clanovi
# #Izmena kraj


        conn.send(odgovor_klijentu.encode())
        conn.close()
        server_ispis_text.insert(END,time.strftime("%H:%M:%S",time.localtime())+" Klijent "+zahtev_klijenta+"\n")
        server_ispis_text.insert(END,time.strftime("%H:%M:%S",time.localtime())+" Server "+odgovor_klijentu+"\n")
        server_ispis_text.see(END)

prozor=tkinter.Tk()
dictDonacije={}
suma=0
s=socket.socket()
host=socket.gethostname()
port=9990
s.bind((host,port))
s.listen(5)
threading.Thread(target=serverNit, daemon=True).start()

prozor.title("Sever prozor")
#prozor.geometry("100x800")
prozor.geometry("800x100")
prozor.resizable(0,0)
server_ispis_text=Text(prozor)
server_ispis_text.pack(pady=10)
prozor.mainloop()

#PIT_Stevan_Vucenovic_RIN819_seminarski1
