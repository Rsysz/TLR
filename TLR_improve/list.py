import os
from os import listdir

path_root = './Annotations/'
files = listdir(path_root)
path = os.path.abspath('.')
save = open("list.txt", 'w')
for i in files:
	line=path+'\\'+i[0:-4]+'.jpg\n'
	save.write(line)

