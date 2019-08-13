import xml.etree.cElementTree as ET
import os
import re
path_root = ['Annotations']
txt_path = './txtout2/'
image_paht = './data/obj/'
dict = {"Traffic Light": "0",
        "Red":"1",
        "Yellow":"2",
        "Green":"3",
        "Right":"6",
        "Straight":"4",
        "Left":"5",}

for anno_path in path_root:
    #save = open("output.txt", 'w')
    xml_list = os.listdir(anno_path)
    save2 = open("data.txt", 'w')
    for axml in xml_list:        
        path_xml = os.path.join(anno_path, axml)
        tree = ET.parse(path_xml)
        root = tree.getroot()

        for child in root.findall('filename'):
            filename = child.text        
            save = open(txt_path+filename[31:-4]+".txt", 'w')
            line2 = image_paht+filename[31:-4]+'.jpg\n'
            save2.write(line2)
            flag = 0
        for child in root.findall('size'):
            width = float(child.find('width').text)
            height = float(child.find('height').text)

        for child in root.findall('object'):
            if flag:
                line = '\n'
            else:
                line = ''
            name = child.find('name').text
            bndbox=child.find('bndbox')
            xmin = float(bndbox.find('xmin').text)
            ymin = float(bndbox.find('ymin').text)
            xmax = float(bndbox.find('xmax').text)
            ymax = float(bndbox.find('ymax').text)

            dw = 1./width
            dh = 1./height
            x = (xmin + xmax)/2.0
            y = (ymin + ymax)/2.0
            w = xmax - xmin
            h = ymax - ymin
            x = x*dw
            w = w*dw
            y = y*dh
            h = h*dh

            flag = 1
            line += dict[name]+' '+str(x)[0:7]+' '+str(y)[0:7]+' '+str(w)[0:7]+' '+str(h)[0:7]
            save.write(line)
