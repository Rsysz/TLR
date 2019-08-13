import xml.etree.cElementTree as ET
import os
import re
import cv2
from os import listdir
from os.path import isfile, isdir, join

path_root = ['../1102/full/Annotations']
txt_path = "./renametxt/"
files = listdir(txt_path)
image_path = '../1102/full/JPEGImages/'
draw_path = './result/'
dict = {"Traffic Light": "0",
        "Red":"1",
        "Yellow":"2",
        "Green":"3",
        "Right":"4",
        "Straight":"5",
        "Left":"6"}

count = 0
progress = 0

for f in files:
    count+=1
    #print(f)
    oneline = re.split('\.',f)
    #print(oneline[0])
    myfile = open(txt_path+f,'r')
    inf = myfile.readlines()
    myfile = open(txt_path+f)
    lines = len(myfile.readlines())
    #print(lines)
    tree = ET.parse("../1102/full/Annotations/"+oneline[0][0:-2]+".xml")
    root = tree.getroot()
    n= 0
    for child in root.findall('object'):
        name = child.find('name').text
        bndbox=child.find('bndbox')
        x1 = bndbox.find('xmin').text
        y1 = bndbox.find('ymin').text
        x2 = bndbox.find('xmax').text
        y2 = bndbox.find('ymax').text
        increasex=int((int(x2)-int(x1))*2)
        increasey=int((int(y2)-int(y1))*3)
        cropx1 = int(x1) - increasex
        cropx2 = int(x2) + increasex
        cropy1 = int(y1) - increasey
        cropy2 = int(y2) + increasey
        if cropx1 < 0:
            cropx1 = 0
        if cropx2 > 2048:
            cropx2 = 2048
        if cropy1 < 0:
            cropy1 = 0
        if cropy2 > 1536:
            cropy2 = 1536
        #print("gt: crop",cropx1,cropy1,cropx2,cropy2)
        if  oneline[0][-1] == '0':
            image = cv2.imread(image_path+oneline[0][0:-2]+".jpg")
            #print(oneline[0][-1])
        else:
            image = cv2.imread(draw_path+oneline[0][0:-2]+".jpg")
            #print(oneline[0][-1])
        if str(n) == oneline[0][-1]:
            for i in range(lines):        
                inputline = re.split(' |\n',inf[i])
                name = inputline[0]
                xmin = int(inputline[2])
                ymin = int(inputline[3])
                xmax = int(inputline[4])
                ymax = int(inputline[5])
                #print("dt:",name,xmin+cropx1,ymin+cropy1,xmax+cropx1,ymax+cropy1)
                if name == 'Red':
                    color = (0, 0, 255)
                elif name == 'Yellow':
                    color = (0, 255, 255)
                elif name == 'Green': 
                    color = (0, 255, 0)
                elif name == 'Left':
                    color = (189, 183,107)
                elif name == 'Straight':
                    color = (39, 139, 34)
                elif name == 'Right':
                    color = (32, 178, 170)
                else:
                    color = (18, 153, 255)
                image = cv2.rectangle(image,(int((xmin+cropx1)),
                                             int((ymin+cropy1))),
                                            (int((xmax+cropx1)),
                                             int((ymax+cropy1))), color, 2)
            #print(inputline)
            cv2.imwrite(draw_path+oneline[0][0:-2]+".jpg", image)
        n+=1
