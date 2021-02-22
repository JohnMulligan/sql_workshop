import sys
from PIL import Image
import os
import re
import shutil
import sqlite3
from optparse import OptionParser, Option, OptionValueError
import time
from shutil import copyfile


parser = OptionParser()
parser.add_option("-d", action="store", type="str", dest="destination_directory", default="/Volumes/research/jcm10/herschels/dec30test/")
(options, args) = parser.parse_args()

#d variable points to the destination directory 
#s variable to True makes it a single loop, False allows for photo stitching

cnx = sqlite3.connect('herschel_data.db')
cursor = cnx.cursor()
tempdir = './herschel_temp'
screenshotdir=os.path.expanduser('~/Desktop')

destination_directory=options.destination_directory
print(os.listdir(screenshotdir))

#hard-coded to allow for a manual switch between different image capture runs
#(I had to do one with Caroline and one with William)
suffix="William"


def main():
	
	sweep_ids = [i[0] for i in cursor.execute("SELECT sweep_id FROM sweeps;").fetchall()]
	
	print("database contains %d sweeps" %len(sweep_ids))
	
	images_sweep_ids = [i[0] for i in cursor.execute("SELECT DISTINCT sweep_id FROM screenshots;").fetchall()]
	
	sweeps_without_images=list(set(sweep_ids)-set(images_sweep_ids))
	
	print("%d sweeps have associated image pointers; %d do not" %(len(sweep_ids)-len(sweeps_without_images),len(sweeps_without_images)))
	
	sweep_ints=list(set([int(re.search('(?<=Sweep)[0-9]+',i).group(0)) for i in sweeps_without_images]))
	
	sweep_ints.sort()
	
	sorted_sweep_ids = []
		
	for sweep_int in sweep_ints:
		try:
			basematch=[i for i in sweep_ids if re.match('Sweep'+str(sweep_int)+'$',i)][0]
			sorted_sweep_ids.append(basematch)
		except:
			matches = [i for i in sweep_ids if re.fullmatch('Sweep'+str(sweep_int)+'[a-z]+',i)!=None]
			for match in matches:
				sorted_sweep_ids.append(match)
	
	#for i in sorted_sweep_ids:
		#print(i)
	
	#print(sorted_sweep_ids)
		
	image_workflow(sorted_sweep_ids)
	
def checkdesktop():
	
	check=[i for i in os.listdir(screenshotdir) if i.endswith('.png')]
	
	return check

def stitch_and_ship(newfiles,sweep_id):
	
	if len(newfiles) > 0:
		
		min_width=0
		
		outputimagefilename=sweep_id+'_' + suffix +'.png'
		
		outputimagepath=os.path.join(destination_directory,outputimagefilename)
	
		#if we're stitching images, first get the minimum width
	
		for file in newfiles:
		
			image = Image.open(file)
		
			imagewidth,imageheight=image.size
		
			if min_width == 0 or imagewidth < min_width:
			
				min_width = imagewidth
		
			image.close()
	
		total_height = 0
	
		thumbnails = []
	
		#then scale each image down to that minimum width so they'll paste well
		
		#and get the total height along the way
	
		for file in newfiles:
		
			image = Image.open(file)
		
			imagewidth,imageheight = image.size
		
			factor = min_width/imagewidth
		
			newheight = round(imageheight*factor)
		
			image.thumbnail((min_width, newheight),Image.ANTIALIAS)
															
			image.save(file)
		
			total_height += newheight
		
			image.close()
	
		#then create a placeholder image to paste the thumbnail images into
	
		new_image = Image.new('RGB', (min_width,total_height))
	
		y_offset = 0
	
		for file in newfiles:
		
			image = Image.open(file)
		
			width,height=image.size
		
			new_image.paste(image, (0,y_offset,width,height+y_offset))
		
			y_offset += height
		
			image.close()
		
		new_image.save(outputimagepath)
	
		new_image.close()
	
		#now clean up
	
		tempfiles=[i for i in os.listdir(tempdir) if i.endswith('.png')]
		
		for file in tempfiles:
			
			os.remove(os.path.join(tempdir,file))
		
	else:
		
		shutil.copy(newfiles[0],outputimagepath)
		
		os.remove(newfiles[0])
		
def image_workflow(sweep_ids):
	
	if not os.path.exists(tempdir):
		
		os.mkdir(tempdir)
	
	for sweep_id in sweep_ids:
			
		print("take screenshot(s) of: ",sweep_id)

		if re.match('Sweep[0-9]+[a-z]+',sweep_id)!=None:
		
			base_sweep_string=re.sub('[a-z]+$','',sweep_id)
		
			adjacent_strings=[i for i in sweep_ids if re.match(base_sweep_string+'[a-z]+',i)!=None]
		
			print('adjacent sweeps:')
		
			for a in adjacent_strings:
				startRA,endRA = cursor.execute("select startRA,endRA from sweeps where sweep_id=?",[a]).fetchone()
				print(a,startRA,endRA)
				
		while True:	
			
			try:
				check=checkdesktop()
			
				if len(check)==1:
				
					os.rename(os.path.join(screenshotdir,check[0]),os.path.join(tempdir,check[0]))
			
				else:
				
					time.sleep(.1)
		
			except KeyboardInterrupt:
				
				newfiles=[i for i in os.listdir(tempdir) if i.endswith('.png')]
				
				newfiles.sort()
				
				newfilepaths=[os.path.join(tempdir,i) for i in newfiles]
		
				stitch_and_ship(newfilepaths,sweep_id)
				
				break
			
	os.rmdir(tempdir)

if __name__ == "__main__":
	
	main()