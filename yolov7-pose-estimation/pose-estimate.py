import argparse

import os
import json

import cv2
import numpy as np
import torch
from torchvision import transforms

from models.experimental import attempt_load
from utils.datasets import letterbox
from utils.general import non_max_suppression_kpt, strip_optimizer
from utils.plots import output_to_keypoint
from utils.torch_utils import select_device

@torch.no_grad()
def run(poseweights = "yolov7-w6-pose.pt", source = "0", device = 'cpu', view_img = True, save_conf = False, line_thickness = 3, hide_labels = False, hide_conf = True):
    
    device = select_device(opt.device) #select device

    model = attempt_load(poseweights, map_location=device)  #Load model
    _ = model.eval()
   
    if source.isnumeric():    
        cap = cv2.VideoCapture(int(source))    #pass video to videocapture object
    
    else:
        cap = cv2.VideoCapture(source)    #pass video to videocapture object
    
    fps = round(cap.get(cv2.CAP_PROP_FPS), 0)
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    lmList_user = []

    if (cap.isOpened() == False):   #check if videocapture not opened
        print('Error while trying to read video. Please check path again')
        raise SystemExit()

    else:
        frame_width = int(cap.get(3))  #get video frame width
        frame_height = int(cap.get(4)) #get video frame height

        while(cap.isOpened): #loop until cap opened or video not complete

            ret, frame = cap.read()  #get frame and success from video capture

            timestamps = [int(cap.get(cv2.CAP_PROP_POS_MSEC))]

            if timestamps[-1] % 1001 == 0 and ret:
                try:
                    orig_image = frame #store frame
                    image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB) #convert frame to RGB
                    image = letterbox(image, (frame_width), stride=64, auto=True)[0]
                    image = transforms.ToTensor()(image)
                    image = torch.tensor(np.array([image.numpy()]))

                    image = image.to(device)  #convert image data to device
                    image = image.float() #convert image to float precision (cpu)

                    with torch.no_grad():  #get predictions
                        output_data, _ = model(image)

                    output_data = non_max_suppression_kpt(output_data, 0.25, 0.65, nc = model.yaml['nc'], nkpt = model.yaml['nkpt'], kpt_label = True)

                    print(fps, total_frames, timestamps)

                    output = output_to_keypoint(output_data)

                    output = output[output[:,7].argsort()]

                    left = output[0].reshape(-1, 58).tolist()

                    lmlist_leftuser = []

                    for x in left[0][7:]:
                        lmlist_leftuser.append(int(x))

                    del lmlist_leftuser[2::3]

                    for y in lmlist_leftuser:
                        lmList_user.append(y)

                    try:
                        right = output[1].reshape(-1, 58).tolist()

                        lmlist_rightuser = []

                        for y in right[0][7:]:
                            lmlist_rightuser.append(int(y))

                        del lmlist_rightuser[2::3]

                        print(lmlist_rightuser)

                        print("RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")

                    except:
                        pass
                
                except:
                    break

            elif not ret:
                break

        cap.release()

    return lmList_user

def parse_opt(v):
    parser = argparse.ArgumentParser()
    parser.add_argument('--poseweights', nargs='+', type=str, default='yolov7-w6-pose.pt', help='model path(s)')
    parser.add_argument('--source', type=str, default=v, help='video/0 for webcam') #video source
    parser.add_argument('--device', type=str, default='cpu', help='cpu/0,1,2,3(gpu)')   #device arugments
    parser.add_argument('--view-img', action='store_true', help='display results')  #display results
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels') #save confidence in txt writing
    parser.add_argument('--line-thickness', default=3, type=int, help='bounding box thickness (pixels)') #box linethickness
    parser.add_argument('--hide-labels', default=False, action='store_true', help='hide labels') #box hidelabel
    parser.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences') #boxhideconf
    opt = parser.parse_args()
    return opt

#main function
def main(opt):
    return run(**vars(opt))

if __name__ == "__main__":
    cwd = os.getcwd().replace("\\", "/") + "/full_video/"

    onlyfiles = [f for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f))]

    for x in onlyfiles:
        cap = cwd + x

        lmList_user = []

        opt = parse_opt(cap)
        strip_optimizer(opt.device,opt.poseweights)
        lmList_user = main(opt)

        f = open(x + ".json", "x")

        with open(x + ".json", "w") as f:
            json.dump(lmList_user, f)

        f.close()