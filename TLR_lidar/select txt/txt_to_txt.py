import os
import xml.etree.cElementTree as ET
dict = {"Traffic Light": "0",
        "Red":"1",
        "Yellow":"2",
        "Green":"3",
        "Right":"6",
        "Straight":"4",
        "Left":"5",}
flie = open("0422_12mm_lidar_crop_90m.txt","r")
save = open("0422_12mm_test_crop_90m.txt","w")
for i in flie.readlines():
    tree = ET.parse('./Annotations/'+i[32:-5]+'.xml')
    root = tree.getroot()
    line = '0422_12mm_lidar/crop/JPEGImages/' + i[32:-1]
    for child in root.findall('object'):
        name = child.find('name').text
        bndbox=child.find('bndbox')
        xmin = (bndbox.find('xmin').text)
        ymin = (bndbox.find('ymin').text)
        xmax = (bndbox.find('xmax').text)
        ymax = (bndbox.find('ymax').text)
        line += ' '+xmin+','+ymin+','+xmax+','+ymax+','+dict[name]
        for child in child.findall('status'):
            name = child.find('name').text
            bndbox=child.find('bndbox')
            xmin = (bndbox.find('xmin').text)
            ymin = (bndbox.find('ymin').text)
            xmax = (bndbox.find('xmax').text)
            ymax = (bndbox.find('ymax').text)

            line += ' '+xmin+','+ymin+','+xmax+','+ymax+','+dict[name]

    line +='\n'
    save.write(line)
    #print(line,end='')

    # inputflie = open("0422_12mm_lidar_crop_105m.txt","r")