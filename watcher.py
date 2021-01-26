import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import sys
import shutil
import logging
from datetime import datetime,timedelta
#print(os.getcwd())
#os.chdir('~/')
class MyHandler(FileSystemEventHandler):
	def on_modified(self,event):
		#This are the extensions that are going to be tracked and where they should be stored
		#".extension":"path/to/directory"
		#This will clean whatever directory it is run from eg. Desktop,Downlods,/home etc 
		#We can move all this files to a different mount point 
		#HOME = "/media/cephas/CEPHAS1/"  
		#For demonstration I am saving the files on my home directory under sorted directory.ie ~/Sorted/file_directory
		HOME = os.getenv("HOME")# change this path to where you want your files stored
		#HOME = "/media/cephas/CEPHAS1/"
		extensions = {
		".py" :	 "Sorted/pythonFiles",
		".java": "Sorted/java",
		".class": "Sorted/java",
		".jpg":  "Sorted/images",
		".jpeg": "Sorted/images",
		".png":  "Sorted/images",
		".svg": "Sorted/images",
		".html": "Sorted/htmlFiles",
		".sh":   "Sorted/bash",
		".pl" :  "Sorted/perl",
		".mkv" : "Sorted/youtube",
		".flv" : "Sorted/youtube",
		".mp4" : "Sorted/youtube",
		".mp3" : "Sorted/youtube",
		"webm" : "Sorted/youtube",
		".pdf" : "Sorted/pdf"

	}
		#Create the path destinations
		for path_keys in extensions:
			destinations = os.path.join(HOME,extensions[path_keys])
			if(os.path.exists(destinations)):
				pass
			else:
				os.makedirs(destinations)
			#print(destinations)	
		time.sleep(60)
		for files in os.listdir('.'):
			j = 1
			i = 1
			#Skip the actual script when moving other files and dot files
			if os.path.isdir(files) or os.path.basename(files) == sys.argv[0]:
				
				pass
			elif (files.startswith('.')):
				pass
			else:
				name_of_file,file_extension = os.path.splitext(files)
				#create a dictionary to store the extensions
				if file_extension in extensions:
					#if extension is being tracked get its destination from predefined once.
					dest = os.path.join(HOME,extensions[file_extension])
					path_dest = os.path.join(dest,files)
					#print(path_dest)
					
                    #if the filename exists append a number to the second file name and save the filename as mod_file
					while os.path.exists(path_dest):
						
						i = i + 1
						mod_file = name_of_file + str(i) + file_extension
						path_dest = os.path.join(dest,mod_file)
						#print(path_dest)
					#pass
				#if the extension is not being tracked ,store them at Misc		
				else:
					
					dest = os.path.join(HOME,"Sorted/Misc")
					if (os.path.exists(dest)):
						pass
					else:
						os.makedirs(dest)
					path_dest = os.path.join(dest,files)
					#append a number if a similar file exists
					while os.path.exists(path_dest):
						j = j+1
						mod_file = name_of_file + str(j) + file_extension
						path_dest = os.path.join(dest,mod_file)
				shutil.move(files,path_dest)

if __name__ == "__main__":
	path = os.getcwd()

	event_handler = MyHandler()
	observer = Observer()
	observer.schedule(event_handler,path,recursive=False)
	observer.start()
	try:
		#time.sleep(10)
		while True:
			time.sleep(5)
	except KeyboardInterrupt:
		observer.stop()
		sys.exit()
	observer.join()	
