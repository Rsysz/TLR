import os
import pexpect
import signal
from pexpect import popen_spawn
import cv2

def convert(size, box):
    top = int((box[1] - box[3]/2.0) * size[0])
    left = int((box[0] - box[2]/2.0) * size[1])
    right = int((box[0] + box[2]/2.0) * size[1])
    bottom = int((box[1] + box[3]/2.0) * size[0])
    return (left,top,right,bottom)

def detect_image(img_path, proc1, proc2):
    proc1.sendline(img_path)
    proc1.expect('Enter Image Path: ')
    tl_labels = os.path.join(os.path.dirname(os.path.dirname(img_path)), 'labels', os.path.splitext(os.path.basename(img_path))[0]) + '.txt'
    result_labels = os.path.join(os.path.dirname(os.path.dirname(img_path)), 'results', os.path.splitext(os.path.basename(img_path))[0]) + '.txt'
    file = open(tl_labels, 'r')
    result_file = open(result_labels, 'w')
    origin = cv2.imread(img_path)

    for line in file.readlines():
        line = line.strip()
        formLine = line.split(' ')
        bb = convert(origin.shape, list(map(float, formLine[1:5])))
        result_file.write(classes[0] + " 1 " + " ".join([str(a) for a in bb]) + '\n')

        crop_tl = origin[bb[1]:bb[3], bb[0]:bb[2]]
        cv2.imwrite('tmp.jpg', crop_tl)
        proc2.sendline(os.path.abspath('tmp.jpg'))
        proc2.expect('Enter Image Path: ')
        file_tl = open('tmp.txt', 'r')
        for tl in file_tl.readlines():
            tl = tl.strip()
            formTl = tl.split(' ')
            b = convert(cv2.imread('tmp.jpg').shape, list(map(float, formTl[1:5])))
            c = (bb[0] + b[0], bb[1] + b[1], bb[0] + b[2], bb[1] + b[3])  # relocate
            result_file.write(subclasses[int(formTl[0])] + " 1 " + " ".join([str(a) for a in c]) + '\n')
    file.close()
    return origin

def calc_mAP(proc1, proc2):
    test = open(eval_path, 'r')
    for img in test.readlines():
        detect_image(img.strip('\n'), proc1, proc2)


classes = ["TrafficLight"]
subclasses = ["Red", "Green", "Yellow", "Straight", "Right", "Left"]
eval_path = './data/voc/test.txt'

FLAGS = None

if __name__ == '__main__':

    model_first = pexpect.popen_spawn.PopenSpawn(
        'darknet.exe detector test data/tl.data cfg/yolov3_first.cfg backup/yolov3_firstv2.weights -thresh 0.5 -dont_show -save_labels')
    model_second = pexpect.popen_spawn.PopenSpawn(
        'darknet.exe detector test data/tlr.data cfg/yolov3_second.cfg backup/yolov3_secondv2.weights -thresh 0.5 -dont_show -save_labels')
    model_first.expect('Enter Image Path: ')
    model_second.expect('Enter Image Path: ')

    calc_mAP(model_first, model_second)

    model_first.kill(sig=signal.SIGTERM)
    model_second.kill(sig=signal.SIGTERM)

