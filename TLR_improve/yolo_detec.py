import os
import pexpect
import signal
import argparse
import numpy as np
from pexpect import popen_spawn
import cv2
from timeit import default_timer as timer
import re

def detect_video(proc1, proc2):
    video_path = input('Enter Video Input Path:')
    output_path = input('Enter Video Output Path:')
    vid = cv2.VideoCapture(video_path)
    if not vid.isOpened():
        raise IOError("Couldn't open webcam or video")
    video_FourCC = int(vid.get(cv2.CAP_PROP_FOURCC))
    video_fps = vid.get(cv2.CAP_PROP_FPS)
    video_size = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
                  int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    isOutput = True if output_path != "" else False
    if isOutput:
        print("!!! TYPE:", type(output_path), type(video_FourCC), type(video_fps), type(video_size))
        out = cv2.VideoWriter(output_path, video_FourCC, video_fps, video_size)
    accum_time = 0
    curr_fps = 0
    fps = "FPS: ??"
    prev_time = timer()
    while True:
        return_value, frame = vid.read()
        if return_value is False:
            vid.release()
            break
        # image = Image.fromarray(frame)
        # image.save('tmp_frame.jpg')
        cv2.imwrite('tmp_frame.jpg', frame)
        result = detect_image(os.path.abspath('tmp_frame.jpg'), proc1, proc2)
        # result = np.asarray(image)
        curr_time = timer()
        exec_time = curr_time - prev_time
        prev_time = curr_time
        accum_time = accum_time + exec_time
        curr_fps = curr_fps + 1
        if accum_time > 1:
            accum_time = accum_time - 1
            fps = "FPS: " + str(curr_fps)
            curr_fps = 0
        cv2.putText(result, text=fps, org=(3, 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.50, color=(255, 0, 0), thickness=2)
        cv2.namedWindow("result", cv2.WINDOW_NORMAL)
        cv2.imshow("result", cv2.resize(result, (1080, 810)))
        if isOutput:
            out.write(result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            vid.release()
            break

def convert(size, box):
    # x_center = box[0] * size[1]
    # y_center = box[1] * size[0]
    # width = box[2] * size[1]
    # height = box[3] * size[0]
    xmin = int((box[0] - box[2]/2.0) * size[1])
    ymin = int((box[1] - box[3]/2.0) * size[0])

    xmax = int((box[0] + box[2]/2.0) * size[1])
    ymax = int((box[1] + box[3]/2.0) * size[0])

    return [xmin,ymin,xmax,ymax]

def detect_image(img_path , proc1, proc2):
    # img_path = input('Enter Image Path:')
    # proc1 = pexpect.popen_spawn.PopenSpawn('darknet.exe detector test data/tl.data cfg/yolov3_first.cfg backup/yolov3_first.weights -thresh 0.5 -dont_show -save_labels')
    
    imagename = img_path.strip()
    name = imagename.split('\\')
    # print(name[-1])
    inputimg = cv2.imread(img_path)
    crop1 = inputimg[0:896, 0:896]
    cv2.imwrite('tmpcrop1.jpg', crop1)
    crop2 = inputimg[0:896, 576:1472]
    cv2.imwrite('tmpcrop2.jpg', crop2)
    crop2 = inputimg[0:896, 1152:2048]
    cv2.imwrite('tmpcrop3.jpg', crop2)

    proc1.sendline(os.path.abspath('tmpcrop2.jpg'))
    proc1.expect('Enter Image Path: ')

    proc1.sendline(os.path.abspath('tmpcrop3.jpg'))
    proc1.expect('Enter Image Path: ')

    proc1.sendline(os.path.abspath('tmpcrop1.jpg'))
    proc1.expect('Enter Image Path: ')


    file_tl2 = open('tmpcrop2.txt', 'r')

    output = open('./output/firstout.txt', 'w')
    x_tmp = ''
    y_tmp = ''
    line = ''
    count_tmp = 0
    for tl2 in file_tl2.readlines():
        tl2 = tl2.strip()
        formTl2 = tl2.split(' ')
        bb_crop2 = convert((896,896), list(map(float, formTl2[1:5])))
        bb_crop2[0]+=576
        bb_crop2[2]+=576
        file_tl1 = open('tmpcrop1.txt', 'r')

        x = (bb_crop2[0] + bb_crop2[2])/2
        y = (bb_crop2[1] + bb_crop2[3])/2


        for tl1 in file_tl1.readlines():
            tl1 = tl1.strip()
            formTl1 = tl1.split(' ')
            bb_crop1 = convert((896,896), list(map(float, formTl1[1:5])))

            x_mean = (bb_crop1[2] + bb_crop1[0])/2
            y_mean = (bb_crop1[3] + bb_crop1[1])/2


            if (x_mean > bb_crop2[0] and y_mean > bb_crop2[1] and x_mean < bb_crop2[2] and y_mean < bb_crop2[3]) or (x > bb_crop1[0] and y > bb_crop1[1] and x < bb_crop1[2] and y < bb_crop1[3]):
                if bb_crop1[0]<bb_crop2[0]:
                    bb_crop2[0] = bb_crop1[0]

                if bb_crop1[1]<bb_crop2[1]:
                    bb_crop2[1] = bb_crop1[1]

                if bb_crop1[2]>bb_crop2[2]:
                    bb_crop2[2] = bb_crop1[2]

                if bb_crop1[3]>bb_crop2[3]:
                    bb_crop2[3] = bb_crop1[3]

                x_tmp += str(x_mean)+' '
                y_tmp += str(y_mean)+' '
                count_tmp += 1

        file_tl1.close()

        file_tl3 = open('tmpcrop3.txt', 'r')
        for tl3 in file_tl3.readlines():
            tl3 = tl3.strip()
            formTl3 = tl3.split(' ')
            bb_crop3 = convert((896,896), list(map(float, formTl3[1:5])))
            bb_crop3[0] +=1152
            bb_crop3[2] +=1152
            x_mean = (bb_crop3[2] + bb_crop3[0])/2
            y_mean = (bb_crop3[3] + bb_crop3[1])/2

            if (x_mean > bb_crop2[0] and y_mean > bb_crop2[1] and x_mean < bb_crop2[2] and y_mean < bb_crop2[3]) or (x > bb_crop3[0] and y > bb_crop3[1] and x < bb_crop3[2] and y < bb_crop3[3]):
                if bb_crop3[0]<bb_crop2[0]:
                    bb_crop2[0] = bb_crop3[0]

                if bb_crop3[1]<bb_crop2[1]:
                    bb_crop3[1] = bb_crop3[1]

                if bb_crop3[2]>bb_crop2[2]:
                    bb_crop3[2] = bb_crop3[2]

                if bb_crop3[3]>bb_crop2[3]:
                    bb_crop2[3] = bb_crop3[3]

                x_tmp += str(x_mean)+' '
                y_tmp += str(y_mean)+' '
                count_tmp += 1

        file_tl3.close()
        line = '0 '+str(bb_crop2[0])+' '+str(bb_crop2[1])+' '+str(bb_crop2[2])+' '+str(bb_crop2[3])+'\n'
        output.write(line)
        # cv2.rectangle(inputimg, (bb_crop2[0], bb_crop2[1]), (bb_crop2[2], bb_crop2[3]), (255, 255, 255),2)
        # cv2.putText(inputimg, classes[0], (bb_crop2[0], bb_crop2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    file_tl2.close()


    file_tl1 = open('tmpcrop1.txt', 'r')

    for tl1 in file_tl1.readlines():
            tl1 = tl1.strip()
            formTl1 = tl1.split(' ')
            bb_crop1 = convert((896,896), list(map(float, formTl1[1:5])))

            x_mean = (bb_crop1[2] + bb_crop1[0])/2
            y_mean = (bb_crop1[3] + bb_crop1[1])/2
            flag = 0
            for i in range(count_tmp):
                x = x_tmp.strip()
                formx = x.split(' ')
                y = y_tmp.strip()
                formy = y.split(' ')

                if float(formx[i]) == x_mean and float(formy[i]) == y_mean:
                    flag = 1
            if flag == 1:
                continue
            line = '0 '+str(bb_crop1[0])+' '+str(bb_crop1[1])+' '+str(bb_crop1[2])+' '+str(bb_crop1[3])+'\n'
            output.write(line)
            # cv2.rectangle(inputimg, (bb_crop1[0], bb_crop1[1]), (bb_crop1[2], bb_crop1[3]), (255, 255, 255),2)
            # cv2.putText(inputimg, classes[0], (bb_crop1[0], bb_crop1[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)           

    file_tl1.close()

    file_tl3 = open('tmpcrop3.txt', 'r')

    for tl3 in file_tl3.readlines():
            tl3 = tl3.strip()
            formTl3 = tl3.split(' ')
            bb_crop3 = convert((896,896), list(map(float, formTl3[1:5])))
            # print(bb_crop3)

            x_mean = (bb_crop3[2] + bb_crop3[0])/2+1152
            y_mean = (bb_crop3[3] + bb_crop3[1])/2
            flag = 0
            for i in range(count_tmp):
                x = x_tmp.strip()
                formx = x.split(' ')
                y = y_tmp.strip()
                formy = y.split(' ')

                if float(formx[i]) == x_mean and float(formy[i]) == y_mean:
                    flag = 1
            if flag == 1:
                continue
            line = '0 '+str(int(bb_crop3[0])+1152)+' '+str(int(bb_crop3[1]))+' '+str(int(bb_crop3[2])+1152)+' '+str(int(bb_crop3[3]))+'\n'
            output.write(line)
            # cv2.rectangle(inputimg, (bb_crop3[0], bb_crop3[1]), (bb_crop3[2], bb_crop3[3]), (255, 255, 255),2)
            # cv2.putText(inputimg, classes[0], (bb_crop3[0], bb_crop3[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)           

    file_tl3.close()

    output.close()


    first = open('./output/firstout.txt', 'r')
    output = open('./output/'+name[-1][0:-4]+'.txt', 'w')
    for line in first.readlines():
        line = line.strip()
        formLine = line.split(' ')
        # print("formLine"+str(formLine))
        bb = convert(inputimg.shape, list(map(float, formLine[1:5])))
        # print(formLine[2],formLine[4], formLine[1],formLine[3])
        crop_tl = inputimg[int(formLine[2]):int(formLine[4]), int(formLine[1]):int(formLine[3])]
        cv2.imwrite('secondtmp.jpg', crop_tl)
        proc2.sendline(os.path.abspath('secondtmp.jpg'))
        proc2.expect('Enter Image Path: ')
        file_tl = open('secondtmp.txt', 'r')
        for tl in file_tl.readlines():
            tl = tl.strip()
            formTl = tl.split(' ')
            b = convert(cv2.imread('secondtmp.jpg').shape, list(map(float, formTl[1:5])))

            cv2.rectangle(inputimg, (b[0] +int(formLine[1]), b[1] +int(formLine[2])), (b[2] + int(formLine[1]), b[3] + int(formLine[2])), dict[int(formTl[0])],2)
            cv2.putText(inputimg, subclasses[int(formTl[0])], (b[0]+int(formLine[1]), int(formLine[4])+b[3] ), cv2.FONT_HERSHEY_SIMPLEX, 0.5,dict[int(formTl[0])], 1, cv2.LINE_AA)

            line = str(int(formTl[0])+1)+' 1 '+str(b[0] +int(formLine[1]))+' '+str(b[1] +int(formLine[2]))+' '+str(b[2] + int(formLine[1]))+' '+str( b[3] + int(formLine[2]))+'\n'
            output.write(line)
        cv2.rectangle(inputimg, (int(formLine[1]), int(formLine[2])), (int(formLine[3]), int(formLine[4])), (255, 255, 255),2)
        cv2.putText(inputimg, classes[0], (int(formLine[1]), int(formLine[2])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        line = formLine[0]+' 1 '+formLine[1]+' '+formLine[2]+' '+formLine[3]+' '+formLine[4]+'\n'
        output.write(line)
    first.close()
    
    return inputimg


classes = ["Traffic Light"]
subclasses = ["R", "G", "Y", "S", "R", "L"]
dict ={ 0:(255,144,30),
        1:(0,165,255), 
        2:(0,0,255),
        3:(211,0,148), 
        4:(238,104,123), 
        5:(12,149,205)}

FLAGS = None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument(
        '--video', default=False, action="store_true",
        help='Video detection mode'
    )
    FLAGS = parser.parse_args()
    # model ready and standby
    model_first = pexpect.popen_spawn.PopenSpawn('darknet.exe detector test data/obj.data yolo-obj1.cfg backup/first/yolo-obj_final1.weights -thresh 0.5 -dont_show -save_labels')
    # model_first = pexpect.popen_spawn.PopenSpawn('darknet.exe detector test data/obj.data yolo-obj2.cfg backup/first/yolo-obj_final2.weights -thresh 0.5 -dont_show -save_labels')
    model_first.expect('Enter Image Path: ')
    model_second = pexpect.popen_spawn.PopenSpawn('darknet.exe detector test data/obj_second.data yolov3_second.cfg backup/second/yolo-obj_final.weights -thresh 0.5 -dont_show -save_labels')
    model_second.expect('Enter Image Path: ')
    if FLAGS.video:
        print("Video detection mode\n")
        detect_video(model_first, model_second)
    else:
        print("Image detection mode\n")
        while True:
            img_path = input('Enter Image Path:')
            result = detect_image(img_path, model_first, model_second)
            cv2.imwrite(img_path+'result.jpg', result)
            # cv2.namedWindow("result", cv2.WINDOW_NORMAL)
            # cv2.imshow("result", cv2.resize(result, (1080, 810)))
            # cv2.waitKey()
            # cv2.destroyAllWindows()
    model_first.kill(sig=signal.SIGTERM)
