import xml.etree.cElementTree as ET
import os
from os import listdir
from os.path import isfile, isdir, join
import re
path_root = './Annotations/'
txt_path = './txtout/'
dict = {"Traffic Light": "0",
        "Red":"1",
        "Green":"2",
        "Yellow":"3",
        "Straight":"4",
        "Right":"5",
        "Left":"6"}
files = listdir(path_root)
inputtxt = open("test.txt", 'r')
for i in files:
    # print(i[0:-4])
    # print(lines)
    # print(lines[-2][0:-4])
    tree = ET.parse(path_root+i[0:-4]+'.xml')
    root = tree.getroot()
    save = open(txt_path+i[0:-4]+".txt", 'w')
    line =''
    for child in root.findall('object'):
        name = child.find('name').text
        bndbox=child.find('bndbox')
        xmin = (bndbox.find('xmin').text)
        ymin = (bndbox.find('ymin').text)
        xmax = (bndbox.find('xmax').text)
        ymax = (bndbox.find('ymax').text)
        if int(ymax) - int(ymin) <= 5:
            continue
        line += dict[name]+' '+xmin+' '+ymin+' '+xmax+' '+ymax+'\n'
        for child2 in child.findall('status'):
            name = child2.find('name').text
            bndbox=child2.find('bndbox')
            xmin = (bndbox.find('xmin').text)
            ymin = (bndbox.find('ymin').text)
            xmax = (bndbox.find('xmax').text)
            ymax = (bndbox.find('ymax').text)
            line += dict[name]+' '+xmin+' '+ymin+' '+xmax+' '+ymax+'\n'
    save.write(line)
