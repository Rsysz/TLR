import xml.etree.ElementTree as ET
import pickle
import os
import cv2
from os import listdir, getcwd
from os.path import join

sets=[('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = ["Traffic Light"]

subclasses = ["Red", "Green", "Yellow", "Straight", "Right", "Left"]

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_images(year, image_id):
    img_file = cv2.imread('VOCdevkit/VOC%s/JPEGImages/%s.jpg'%(year, image_id))
    in_file = open('VOCdevkit/VOC%s/Annotations/%s.xml'%(year, image_id), encoding='UTF-8')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    num = 0
    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in classes:
            continue
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymin').text), int(xmlbox.find('ymax').text))
        if b[3] - b[2] < 5:
            continue
        crop_img = img_file[b[2]:b[3], b[0]:b[1]]
        out_file = open('VOCdevkit/VOC%s/Crop_labels/%s_%d.txt' % (year, image_id, num), 'w')
        for status in obj.findall('status'):
            if status is None:
                continue
            light = status.find('name').text
            cls_id = subclasses.index(light)
            xmlbox = status.find('bndbox')
            c = (float(xmlbox.find('xmin').text) - b[0], float(xmlbox.find('xmax').text) - b[0], float(xmlbox.find('ymin').text) - b[2], float(xmlbox.find('ymax').text) - b[2])
            bb = convert((b[1] - b[0], b[3] - b[2]), c)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
        cv2.imwrite('VOCdevkit/VOC%s/Crop/%s_%d.jpg' % (year, image_id, num), crop_img)
        list_file.write('%s/VOCdevkit/VOC%s/JPEGImages/%s_%d.jpg\n' % (wd, year, image_id, num))
        num += 1


wd = getcwd()

for year, image_set in sets:
    if not os.path.exists('VOCdevkit/VOC%s/labels/'%(year)):
        os.makedirs('VOCdevkit/VOC%s/labels/'%(year))
    image_ids = open('VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%(year, image_set)).read().strip().split()
    list_file = open('%s_%s.txt'%(year, image_set), 'w')
    for image_id in image_ids:
        convert_images(year, image_id)
    list_file.close()
