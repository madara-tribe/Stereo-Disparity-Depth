import time
import cv2
import numpy as np
import onnxruntime
from yolov7s.common import letterbox, preprocess, onnx_inference, post_process
from yolov7s.dist_calcurator import prams_calcurator


    
def load_caps(vid_path, start_time):
    capR = cv2.VideoCapture(vid_path)
    capR.set(cv2.CAP_PROP_POS_FRAMES, start_time * 30)
    return capR

def inference_(frame, session, new_shape, conf_thres):
    ori_images = [frame.copy()]
    resized_image, ratio, dwdh = letterbox(frame, new_shape=new_shape, auto=False)
    input_tensor = preprocess(resized_image)
    outputs = onnx_inference(session, input_tensor)
    pred_output, coordinate_x, coordinate_y, range = post_process(outputs, ori_images, ratio, dwdh, conf_thres)
    return pred_output, coordinate_x, coordinate_y, range
    


    
def video_inference(opt):
    onnx_path = opt.onnx_path
    per_frames = opt.per_frames
    conf_thres = opt.conf_thres
    max_disparity = opt.max_disparity
    min_disparity = opt.min_disparity
    cuda = False if opt.cpu=='True' else True
    start_time = 0
    capR = load_caps(vid_path=opt.rvid_path, start_time=start_time)
    capL = load_caps(vid_path=opt.lvid_path, start_time=start_time)
    providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'] if cuda else ['CPUExecutionProvider']
    session = onnxruntime.InferenceSession(onnx_path, providers=providers)

    IN_IMAGE_H = session.get_inputs()[0].shape[2]
    IN_IMAGE_W = session.get_inputs()[0].shape[3]
    new_shape = (IN_IMAGE_W, IN_IMAGE_H)
    
    Rstack = []
    Lstack = []
    cv2.namedWindow("Detected Objects", cv2.WINDOW_NORMAL)
    c = 1
    while capR.isOpened() and capL.isOpened():
        try:
            retR, frame_right = capR.read()
            retL, frame_left = capL.read()
            Rstack.append(frame_right)
            Lstack.append(frame_left)
            if not retR and not retL:
                break
        except Exception as e:
            print(e)
            continue
        if len(Rstack)==per_frames and len(Lstack)==per_frames:
            # inference each frame
            Routput, Rx, Ry, Rrange = inference_(Rstack[-1], session, new_shape, conf_thres)
            Loutput, Lx, Ly, Lrange = inference_(Lstack[-1], session, new_shape, conf_thres)
            frames = cv2.addWeighted(src1=Routput[0],alpha=0.5,src2=Loutput[0],beta=0.5,gamma=0)
            Rstack, Lstack =[], []
            if abs(Rx-Lx) >=0 or Lx < Rrange or Rx < Lrange:
                disparity = abs(Rx-Lx)
                if disparity <= max_disparity and disparity > min_disparity:
                    h, w = frames.shape[:2]
                    distance, angleX, angleY = prams_calcurator(disparity, width=w, x=Rx, y=Ry)
                    texts = 'disp:{}, distance(z):{}, angleX:{}, angleY : {}'.format(disparity, distance, angleX, angleY)
                    rframe = cv2.circle(Routput[0], (int(Rx), int(Ry)), int(20),(0, 255, 255), 2)
                    lframe = cv2.circle(Loutput[0], (int(Lx), int(Ly)), int(20),(0, 255, 255), 2)
                    #frames = np.concatenate((rframe, lframe), axis=1)
                    frames = cv2.addWeighted(src1=rframe,alpha=0.5,src2=lframe,beta=0.5,gamma=0)
                    cv2.putText(frames, texts, (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 1, [225, 255, 255],thickness=2)
            cv2.imshow("Detected Objects", frames)
            cv2.imwrite('results/frame_{}.png'.format(c), frames)
            c +=1
        if cv2.waitKey(30) == 27:
            break
    capR.release()
    capL.release()

