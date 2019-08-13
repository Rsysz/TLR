import xml.etree.cElementTree as ET
import os
import re
path_root = './VOCdevkit/VOC2007/Annotations/'
txt_path = './txtout/'
dict = {"Traffic Light": "TrafficLight",
        "Red":"Red",
        "Green":"Green",
        "Yellow":"Yellow",
        "Straight":"Straight",
        "Right":"Right",
        "Left":"Left"}

inputtxt = open("test.txt", 'r')
for i in inputtxt.readlines():
    lines =  re.split('/|\n',i)
    # print(lines)
    # print(lines[-2][0:-4])
    tree = ET.parse(path_root+lines[-2][0:-4]+'.xml')
    root = tree.getroot()
    for child in root.findall('filename'):
        #print(axml)
        filename = child.text        
        save = open(txt_path+lines[-2][0:-4]+".txt", 'w')
    line =''
    for child in root.findall('object'):
        name = child.find('name').text
        bndbox=child.find('bndbox')
        xmin = (bndbox.find('xmin').text)
        ymin = (bndbox.find('ymin').text)
        xmax = (bndbox.find('xmax').text)
        ymax = (bndbox.find('ymax').text)
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
