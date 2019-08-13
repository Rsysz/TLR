import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

def find():
    train = pd.read_csv(r'data/train_labels.csv', dtype=str)
    
    data = pd.DataFrame()
    data['format'] = []
    
    # as the images are in train_images folder, add train_images before the image name
#    for i in range(data.shape[0]):
#        #data['format'][i] = 'D:/Datasets/' + data['format'][i]
#        data['format'][i] = data['format'][i] + ' '
    
    # add xmin, ymin, xmax, ymax and class as per the format required
    
    index = 0
    for i in range(train.shape[0]):
    	if (train['class'][i] == '0'):
    		diff = int(train['ymax'][i]) - int(train['ymin'][i])
    	
    		if ( ((diff <= 9) or (int(train['width'][i]) < 40) or (int(train['height'][i]) < 29)) ) :
    			string = train['filename'][i]
    			
    			string = string[31:len(string)-4]
    			
    			data['format'][index] = string
    			
    			index = index + 1
    		
    print (data['format'].shape[0])
    data['format'].to_csv('remove.txt', header=False, index=False)

def remove():
	fp = open('0422_12mm_lidar_crop_error.txt', "r")
	line = fp.readline()
	 
	## 用 while 逐行讀取檔案內容，直至檔案結尾
	while line:
		#print line
		line = line.rstrip('\n')
		try:
			os.remove('Annotations/' + line + '.xml')
			os.remove('JPEGImages/' + line + '.jpg')
			print ("remove file ->  " + line)
		except OSError as e:
			print(e)
		line = fp.readline()


	fp.close()



def main():
	#find()
	remove()


main()