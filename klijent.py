import tkinter
from tkinter import font
from tkinter import *
from tkinter import messagebox
import threading
import socket
import time
import re

def pomeraj_text(labela):
    print(prozor.winfo_height())
    print(prozor.winfo_width())
    while True:
        for i in range(1,50,1):
            labela.place(y=i)
            time.sleep(.1)
        for i in range(50,1,-1):
            labela.place(y=i)
            time.sleep(.1)

def proveri_text(neki_string):
    x = re.match(r"^[a-zA-Z0-9]+[a-zA-Z0-9 ]*$", neki_string)
    if x:
        return True
    else:
        messagebox.showinfo(message="Naziv ne sme biti prazan i moze da sadrzi slova i brojeve!")
        return False
def proveri_broj(neki_broj):
    if neki_broj.isdigit():
        return True
    else:
        messagebox.showinfo(message="Unesti broj nije ispravan!")
        return False

def nova_baza():
    print("Kreiraj novu bazu")
    upit1="DROP TABLE IF EXISTS Automobil"
    upit2='CREATE TABLE Automobil(id int PRIMARY KEY NOT NULL, naziv varchar(50) NOT NULL, cena int)'
    posaljiServeru(upit1)
    posaljiServeru(upit2)



def novi_auto():
    provera=[]
    provera.append(proveri_text(varNaziv.get()))
    provera.append(proveri_broj(varID.get()))
    provera.append(proveri_broj(varCena.get()))
    if all(provera):
        print("novi auto",int(varID.get()),varNaziv.get(),int(varCena.get()))
        n="'"+varNaziv.get()+"'"
        upit="INSERT INTO Automobil (id, naziv, cena) VALUES ("+varID.get()+","+n+","+varCena.get()+")"
        print(upit)
        posaljiServeru(upit)



def novi_select():
    izbor=varKriterijum.get()

    print("Select",izbor,varKriterijumEntry.get())
    upit=""

    if izbor:
        if proveri_text(varKriterijumEntry.get()):
            upit="SELECT * FROM Automobil WHERE naziv='"+varKriterijumEntry.get()+"'"
            print(upit)
            posaljiServeru(upit)

    else:
        if proveri_broj(varKriterijumEntry.get()):
            upit="SELECT * FROM Automobil WHERE id="+varKriterijumEntry.get()
            print(upit)
            posaljiServeru(upit)




def update():

    provera=[]
    provera.append(proveri_broj(varIDpromeni_cenu.get()))
    provera.append(proveri_text(varCenapromeni_cenu.get()))
    if all(provera):
        print("Update",int(varIDpromeni_cenu.get()),varCenapromeni_cenu.get())
        upit="UPDATE Automobil SET naziv='"+varCenapromeni_cenu.get()+"'"+" WHERE id="+varIDpromeni_cenu.get()
        posaljiServeru(upit)

def delete():
    if proveri_text(varNazivobrisi.get()):
        print("Delete", varNazivobrisi.get())
        n = "'" + varNazivobrisi.get() + "'"
        upit="DELETE FROM Automobil WHERE naziv="+n
        posaljiServeru(upit)

def posaljiServeru(string):
    s=socket.socket()
    host=socket.gethostname()
    port=9990
    try:
        s.connect((host,port))
        s.send(string.encode())
        odgovor_servera=s.recv(1024).decode()
        s.close()
    except Exception as e:
        odgovor_servera="Pokrenuti 'server.py' i pokusati ponovo."
    #print(odgovor_servera)
    odgovor_server_text.insert(END, time.strftime("%H:%M:%S", time.localtime()) + " Server " + odgovor_servera + "\n")
    odgovor_server_text.see(END)

def doniraj():
    print("donacija")
    upit="Doniraj "+varDonacijeIme.get()+" "+varDonacijeSuma.get()
    print(upit)
    posaljiServeru(upit)

prozor=tkinter.Tk()
prozor.title("Klijent Prozor")
prozor.resizable(0,0)

varID=StringVar()
varIDpromeni_cenu=StringVar()
varCenapromeni_cenu=StringVar()
varNazivobrisi=StringVar()
varNaziv=StringVar()
varCena=StringVar()
varKriterijum=IntVar()
varKriterijumEntry=StringVar()
varDonacijeIme=StringVar()
varDonacijeSuma=StringVar()

header=Frame(width=800,height=50, borderwidth = 2)
header.pack_propagate(0)
header.pack()
header.size()
helv = font.Font(family="Helvetica",size=32,weight="bold")
lbl_poruka=Label(master=header, text="Banner koji se pomera",font=helv)
lbl_poruka.place(anchor=CENTER, relx=0.5)

body=Frame(width=800, height=700, borderwidth = 2)
body.pack_propagate(0)
body.pack()
big_red_brn=Button(body,text="PRAZNA TABELA",font=("Consolas", 24, "bold"),bg="red",command=nova_baza)
big_red_brn.pack()
unos_frame=LabelFrame(body,text="Unos automobila:")
unos_frame.pack(fill="both",expand="yes")
#**********************************************************
combo_id_frame=Frame(unos_frame,padx=10, pady=5)
lbl_id=Label(combo_id_frame,text="ID:")
lbl_id.pack(anchor=NW)
textbox_id=Entry(combo_id_frame, textvariable=varID)
textbox_id.pack()
combo_id_frame.pack(side=LEFT)
#*********************************************************
combo_naziv_frame=Frame(unos_frame,padx=10, pady=5)
lbl_naziv=Label(combo_naziv_frame,text="Naziv:")
lbl_naziv.pack(anchor=NW)
textbox_naziv=Entry(combo_naziv_frame, textvariable=varNaziv)
textbox_naziv.pack()
combo_naziv_frame.pack(side=LEFT)
#*****************************************************
combo_cena_frame=Frame(unos_frame,padx=10, pady=5)
lbl_cena=Label(combo_cena_frame,text="Cena:")
lbl_cena.pack(anchor=NW)
textbox_cena=Entry(combo_cena_frame, textvariable=varCena)
textbox_cena.pack()
combo_cena_frame.pack(side=LEFT)

big_green_btn=Button(body,text="Unesi zapis",command=novi_auto)
big_green_btn.pack()
#*****************************************************
procitaj_frame=LabelFrame(body,text="Procitaj auto prema kriterijumu:")
procitaj_frame.pack(fill="both",expand="yes")
combo_select=Frame(procitaj_frame)
combo_select.pack(anchor=W,padx=10, pady=5)
rbID=Radiobutton(combo_select,variable=varKriterijum, text="ID",value=0)
rbID.pack(anchor=W)
rbCena=Radiobutton(combo_select,variable=varKriterijum, text="Naziv",value=1)
rbCena.pack(anchor=W,padx=10, pady=5)
textbox_kriterijum=Entry(combo_select,textvariable=varKriterijumEntry)
textbox_kriterijum.pack(anchor=W)
kriterijum_btn=Button(body,text="SELECCT",command=novi_select)
kriterijum_btn.pack()
#*****************************
izmena_cene_frame=LabelFrame(body,text="Promeni naziv automobila po ID:")
izmena_cene_frame.pack(fill="both",expand="yes")

combo_id_izmena_cene_frame=Frame(izmena_cene_frame)
lbl_id_izmena_cene=Label(combo_id_izmena_cene_frame,text="ID:")
lbl_id_izmena_cene.pack(anchor=NW)
textbox_id_izmena_cene=Entry(combo_id_izmena_cene_frame, textvariable=varIDpromeni_cenu)
textbox_id_izmena_cene.pack()
combo_id_izmena_cene_frame.pack(side=LEFT,padx=10, pady=5)

combo_cena_izmena_cene_frame=Frame(izmena_cene_frame)
lbl_cena_izmena_cene=Label(combo_cena_izmena_cene_frame,text="Novi naziv:")
lbl_cena_izmena_cene.pack(anchor=NW)
textbox_cena_izmena_cene=Entry(combo_cena_izmena_cene_frame, textvariable=varCenapromeni_cenu)
textbox_cena_izmena_cene.pack()
combo_cena_izmena_cene_frame.pack(side=LEFT)

izmeni_cenu_btn=Button(body,text="UPDATE",command=update)
izmeni_cenu_btn.pack()
#***********************************************
obrisi_frame=LabelFrame(body,text="Obrisi automobil po filtru:",padx=10, pady=5)
obrisi_frame.pack(fill="both",expand="yes")
lbl_naziv_obrisi=Label(obrisi_frame, text="Naziv:")
lbl_naziv_obrisi.pack(anchor=NW)
textbox_naziv_obrisi=Entry(obrisi_frame, textvariable=varNazivobrisi)
textbox_naziv_obrisi.pack(anchor=W)
obrisi_btn=Button(body,text="DELETE",command=delete)
obrisi_btn.pack()
#**********************************************

# #Modifikacija prilikom odbrane projekta:
#
# donacije_frame=LabelFrame(body,text="Donacije", padx=10, pady=5)
# donacije_frame.pack(fill="both",expand="yes")
# textbox_donacija_ime=Entry(donacije_frame,textvariable=varDonacijeIme)
# textbox_donacija_ime.pack()
# textbox_donacija_suma=Entry(donacije_frame,textvariable=varDonacijeSuma)
# textbox_donacija_suma.pack()
# btn_doniraj=Button(donacije_frame,text="Doniraj",command=doniraj)
# btn_doniraj.pack()


odgovor_server_text=Text(body, height=6)
odgovor_server_text.pack(pady=10)

footer=Frame(width=800, height=50)
footer.pack_propagate(0)
footer.pack()
lbl_copy=Label(master=footer, text="© 2020 Stefan Vucenovic RIN 8/19")
lbl_copy.place(rely=0.5, relx=0.36)




t=threading.Thread(target=pomeraj_text, args=(lbl_poruka,), daemon=True)
t.start()

prozor.mainloop()