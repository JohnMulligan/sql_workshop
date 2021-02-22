import os
import re
import time
import sqlite3
import threading
from optparse import OptionParser, Option, OptionValueError

parser = OptionParser()
parser.add_option("-d", action="store", type="str", dest="d", default="/Volumes/research/jcm10/herschels/dec30test/")
(options, args) = parser.parse_args()

dir=options.d

cnx = sqlite3.connect('herschel_data.db')


cursor = cnx.cursor()

cursor.execute("delete from screenshots;")

sweep_images=[i for i in os.listdir(dir) if i.endswith('.png')]

for image in sweep_images:
	
	sweep_id = re.search("Sweep[0-9]+[a-z]*",image).group(0)

	
	cursor.execute("insert into screenshots (sweep_id,filename) values(?,?);", [sweep_id,image])
	cnx.commit()
	
	print(sweep_id,image)
