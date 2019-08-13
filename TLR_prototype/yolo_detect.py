import os
import pexpect
import signal
import argparse
import numpy as np
from pexpect import popen_spawn
import cv2
from timeit import default_timer as timer


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
        # cv2.namedWindow("result", cv2.WINDOW_NORMAL)
        cv2.imshow("result", cv2.resize(result, (1440, 1080)))
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
    top = int((box[1] - box[3]/2.0) * size[0])
    left = int((box[0] - box[2]/2.0) * size[1])
    right = int((box[0] + box[2]/2.0) * size[1])
    bottom = int((box[1] + box[3]/2.0) * size[0])
    return (top,left,right,bottom)

def detect_image(img_path , proc1, proc2):
    # img_path = input('Enter Image Path:')
    # proc1 = pexpect.popen_spawn.PopenSpawn('darknet.exe detector test data/tl.data cfg/yolov3_first.cfg backup/yolov3_first.weights -thresh 0.5 -dont_show -save_labels')
    proc1.sendline(img_path)
    proc1.expect('Enter Image Path: ')
    # proc1.kill(sig=signal.SIGTERM)
    if FLAGS.video:
        tl_labels = os.path.splitext(img_path)[0] + '.txt'
    else:
        tl_labels = os.path.join(os.path.dirname(os.path.dirname(img_path)), 'labels', os.path.splitext(os.path.basename(img_path))[0]) + '.txt'
    file = open(tl_labels, 'r')
    origin = cv2.imread(img_path)

    # proc2 = pexpect.popen_spawn.PopenSpawn('darknet.exe detector test data/tlr.data cfg/yolov3_second.cfg backup/yolov3_second.weights -thresh 0.5 -dont_show -save_labels')
    for line in file.readlines():
        line = line.strip()
        formLine = line.split(' ')
        bb = convert(origin.shape, list(map(float, formLine[1:5])))

        crop_tl = origin[bb[0]:bb[3], bb[1]:bb[2]]
        cv2.imwrite('tmp.jpg', crop_tl)
        proc2.sendline(os.path.abspath('tmp.jpg'))
        proc2.expect('Enter Image Path: ')
        file_tl = open('tmp.txt', 'r')
        for tl in file_tl.readlines():
            tl = tl.strip()
            formTl = tl.split(' ')
            b = convert(cv2.imread('tmp.jpg').shape, list(map(float, formTl[1:5])))

            cv2.rectangle(origin, (b[1] + bb[1], b[0] + bb[0]), (b[2] + bb[1], b[3] + bb[0]), (0, 77, 255))
            cv2.putText(origin, subclasses[int(formTl[0])], (b[2] + bb[1], b[3] + bb[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 77, 255), 1, cv2.LINE_AA)
        cv2.rectangle(origin, (bb[1], bb[0]), (bb[2], bb[3]), (255, 255, 255))
        cv2.putText(origin, classes[0], (bb[1], bb[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    file.close()
    return origin


classes = ["Traffic Light"]
subclasses = ["Red", "Green", "Yellow", "Straight", "Right", "Left"]

FLAGS = None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument(
        '--video', default=False, action="store_true",
        help='Video detection mode'
    )
    FLAGS = parser.parse_args()
    # model ready and standby
    model_first = pexpect.popen_spawn.PopenSpawn('darknet.exe detector test data/tl.data cfg/yolov3_first.cfg backup/yolov3_firstv2.weights -thresh 0.5 -dont_show -save_labels')
    model_second = pexpect.popen_spawn.PopenSpawn('darknet.exe detector test data/tlr.data cfg/yolov3_second.cfg backup/yolov3_secondv2.weights -thresh 0.5 -dont_show -save_labels')
    model_first.expect('Enter Image Path: ')
    model_second.expect('Enter Image Path: ')

    if FLAGS.video:
        print("Video detection mode\n")
        detect_video(model_first, model_second)
    else:
        print("Image detection mode\n")
        while True:
            img_path = input('Enter Image Path:')
            result = detect_image(img_path, model_first, model_second)
            cv2.imwrite('result.jpg', result)
            # cv2.namedWindow("result", cv2.WINDOW_NORMAL)
            cv2.imshow("result", cv2.resize(result, (1440, 1080)))
            cv2.waitKey()
            cv2.destroyAllWindows()
    model_first.kill(sig=signal.SIGTERM)
    model_second.kill(sig=signal.SIGTERM)
