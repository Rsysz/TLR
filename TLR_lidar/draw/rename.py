from xml.dom.minidom import Document
import os
import cv2
import re
from os import listdir
from os.path import isfile, isdir, join

files = listdir("./predicted/")
nametxt = open("1102_demo.txt", 'r')
names = nametxt.readlines()
count = 0
k = 0
for f in files:
	count+=1
print("Total:"+str(count))


for i in range(count):
	oneline = re.split(' |/|\.',names[i])
	#print(i)
	f = open("./predicted/"+str(i)+".txt", 'r')
	#print(oneline[3])
	#print(f.read())
	save = open("./renametxt/"+oneline[4]+".txt", 'w')
	save.write(f.read())
