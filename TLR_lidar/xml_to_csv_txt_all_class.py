import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET


def transfer_class(name):
    
    if (name == "Traffic Light"):
        return 0
    elif (name == "Red"):
        return 1
    elif (name == "Yellow"):
        return 2
    elif (name == "Green"):
        return 3
    elif (name == "Straight"):
        return 4
    elif (name == "Left"):
        return 5
    elif (name == "Right"):
        return 6
    else:
        return 'error'
    
    

def generate_csv():

    xml_path = "Annotations"
    xml_list = []
   
    
    for xml_file in glob.glob(xml_path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        for member in root.findall('object'):   
            status_num = len(member.findall('status'))
            filename = root.find('filename').text
            classes = transfer_class(member[0].text)
            width = int(root.find('size')[0].text)
            height = int(root.find('size')[1].text)
            xmin = int(member[1][0].text)
            ymin = int(member[1][1].text)
            xmax = int(member[1][2].text)
            ymax = int(member[1][3].text)
            
            value = (filename, width, height, classes, xmin, ymin, xmax, ymax)
           
            xml_list.append(value)
            
            if (status_num):
                for i in range(status_num):
                    classes = transfer_class(member[2+i][0].text)
                    xmin = int(member[2+i][1][0].text)
                    ymin = int(member[2+i][1][1].text)
                    xmax = int(member[2+i][1][2].text)
                    ymax = int(member[2+i][1][3].text)
                    value = (filename, width, height, classes, xmin, ymin, xmax, ymax)
                    xml_list.append(value)
            
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    xml_df.to_csv('data/train_labels.csv', index=None)

def xml_to_txt():
    train = pd.read_csv(r'data/train_labels.csv', dtype=str)
    
    data = pd.DataFrame()
    data['format'] = []
    
    # as the images are in train_images folder, add train_images before the image name
#    for i in range(data.shape[0]):
#        #data['format'][i] = 'D:/Datasets/' + data['format'][i]
#        data['format'][i] = data['format'][i] + ' '
    
    # add xmin, ymin, xmax, ymax and class as per the format required
    
    index = 0
    i = 0
    tmp = train['filename'][0]
    data['format'][index] = train['filename'][0]+ ' '+ train['xmin'][i] + ',' + train['ymin'][i] + ',' + train['xmax'][i] + ',' + train['ymax'][i] + ',' + train['class'][i]
    for i in range(train.shape[0]):
        if (i==0):
            continue
        if (train['filename'][i] == tmp):
            data['format'][index] = data['format'][index] + ' '+ train['xmin'][i] + ',' + train['ymin'][i] + ',' + train['xmax'][i] + ',' + train['ymax'][i] + ',' + train['class'][i]
        else:
            index = index + 1
            tmp = train['filename'][i]
            data['format'][index] = train['filename'][i] + ' '+ train['xmin'][i] + ',' + train['ymin'][i] + ',' + train['xmax'][i] + ',' + train['ymax'][i] + ',' + train['class'][i]
   
    data['format'].to_csv('annotate.txt', header=False, index=False)


def main():
    
    #generate_csv()
    xml_to_txt()
    
main()


    
    
    
    
    
    
    
    
    
