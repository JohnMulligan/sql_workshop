import os
import re
import time
import sqlite3
import threading


#very straightforward, hard-coded, data mapping & import script
##takes Adolfo's default_data.ini file
###(as formatted for the Herschel stellarium plugin)
##parses the file into sweep parameters and values
##checks to see if the sweep exists in herschel_data.db
##if the sweep doesn't exist, it creates an entry with the appropriate values

####this script does not create the properly-formatted database schema!

d = open('default_sweep.ini','r')
t = d.read()
line = t.split("\n")
d.close()

sweeps_dict = {}
for l in line:
	try:
		a,b= l.split('\\')
		
		c,d = b.split('=')
		
		
		
		if c == 'name':
			c='sweep_id'
			d=re.sub(' ','',d)
			
		try:
			sweeps_dict[a][c]=d
		except:
			sweeps_dict[a] = {c:d}

	except:
		pass
	
cnx = sqlite3.connect('herschel_data.db')
cursor = cnx.cursor()

for ini_id in sweeps_dict.keys():
	sweep = sweeps_dict[ini_id]
	sweep_id = sweep['sweep_id']
	check = cursor.execute("SELECT * FROM sweeps WHERE sweep_id='%s';" %sweep_id).fetchone()
	date = sweep['date']
	startDec = sweep['startDec']
	endDec = sweep['endDec']
	startRA = sweep['startRA']
	endRA = sweep['endRA']
	if check == None:
		cursor.execute("INSERT INTO sweeps (sweep_id,date,endDec,startDec,startRA,endRA,youtube_uploaded,tweeted) VALUES (?,?,?,?,?,?,?,?);", [sweep_id,str(date),str(endDec),str(startDec),str(startRA),str(endRA),'FALSE','FALSE'])
		cnx.commit()
		print("new entry:",[sweep_id,str(date),str(endDec),str(startDec),str(startRA),str(endRA),'FALSE','FALSE'])
	else:
		print("entry exists:",check[0])


cnx.close()