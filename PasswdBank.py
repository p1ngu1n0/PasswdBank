#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3, random, string, base64
import os
import sys

W = '\033[0m'  
R = '\033[31m'
G = '\033[32m'  
O = '\033[33m'  
B = '\033[34m' 
P = '\033[35m' 
C = '\033[36m' 


def main():
	global con
	global c

	con = None
	con = sqlite3.connect('src/data.db')
	
	limpiar()

	c = con.cursor()
	c.execute("CREATE TABLE if not exists claves(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, dominio TEXT NOT NULL, usuario TEXT NOT NULL, clave TEXT NOT NULL ) ")
	cifrado()
	menu()
	

def menu():
	Banner()
	while True:
		menu = input(O+"\nroot#: "+W)
		if menu == "gen":
			gen()
		elif menu == "add":
			add()
		elif menu == "view":
			visualizar()
		elif menu == "info":
			info()
		elif menu == "exit":
			close()
		elif menu == "clear":
			limpiar()
		elif menu == "help":
			Banner()
		else:
			limpiar()
			print("Opcion no valida...")

def Banner():
	print(P+"""

  ad8888888888ba
 dP'         `"8b,
 8  ,aaa,       "Y888a     ,aaaa,     ,aaa,  ,aa,
 8  8' `8           "88baadP    YbaaadP   YbdP  Yb
 8  8   8                                        8b
 8  8, ,8         ,aaaaaaaaaaaaaaaaaaaaaaaaddddd88P
 8  `   '       ,d8""
 Yb,         ,ad8"    PasswdBank
  "Y8888888888P"

	-gen   #Genera una clave segura
	-add   #Añade una clave
	-view  #Mira tus claves
	-help  #Ayuda
	-info  #Informacion
	-clear #Limpiar
	-exit  #Salir"""+W)


def info():
	print("Para ayudar al desarrollador, sigueme en https://www.instagram.com/_p1ngu1n0_/")


def limpiar():
	if os.name == "nt":
		os.system("cls")
	elif os.name == "posix":
		os.system("clear")
	else:
		raise("No se puede limpiar la pantalla.")
		print("<--No se puede limpiar la pantalla-->")


def update():
	con.commit()


def cifrado():
	f = open('src/pd.b64', 'r')
	ff = f.read()

	if ff is " ":
		f.close()
		f = open('src/pd.b64', 'wb')
		pwd = input("Nueva clave de acceso: ")
		encode = base64.b64encode(pwd.encode())
		f.write(encode)
		f.close()
		limpiar()
	else:
		inp = input("Clave de acceso: ")
		
		f = open('src/pd.b64', 'rb')
		conten = f.read()
		data = base64.b64encode(inp.encode())
	
		if conten == data:
			limpiar()
			menu()
		else:
			print(R+"Error..."+W)
			close()

	
def visualizar():
	print("(id, dominio, usuario, clave)")
	c.execute("SELECT * FROM claves")
	for reg in c:
		print(P+''.join(str(reg))+W)


def gen():
	try:
		ran = input("Numero de caracteres: ")
		passwd = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(int(ran)))
		print("La clave es: %s" % passwd)
		op = input("Almacenar clave? (S/n): ")
		if op == "s":
			dominio = input("Dominio: ")
			usuario = input("Usuario: ")
			c.execute("INSERT INTO claves (dominio, usuario, clave) VALUES ('"+dominio+"', '"+usuario+"', '"+passwd+"')")
			update()
			print(G+"Almacenado correctamente !"+W)
		elif op == "n":
			menu()
		else:
			print(R+"Error..."+W)

	except ValueError:
		menu()


def add():
	dominio = input("Dominio: ")
	usuario = input("Usuario: ")
	passwd = input("Clave: ")
	c.execute("INSERT INTO claves (dominio, usuario, clave) VALUES ('"+dominio+"', '"+usuario+"', '"+passwd+"')")
	update()
	print(G+"Almacenado correctamente !"+W)


def close():
	con.close()
	limpiar()
	print(R+"\nSaliendo...\n"+W)
	sys.exit()


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		close()
	
