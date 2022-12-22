import argparse
import time
import cv2
import numpy as np
import onnxruntime
import multiprocessing
from common import letterbox, preprocess, onnx_inference, post_process
from dist_calcurator import prams_calcurator

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--onnx_path', type=str, default='yolov7Tiny_640_640.onnx', help='image path')
    parser.add_argument('--cpu', type=str, default='True', help='if cpu is None, use CUDA')
    parser.add_argument('--per_frames', type=int, default=5, help='num frames to predict at each thread for reducing device burden')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='conf threshold for NMS or postprocess')
    parser.add_argument('--max_disparity', type=int, default=240, help='max disparity')
    parser.add_argument('--min_disparity', type=int, default=15, help='min disparity')
    parser.add_argument('--rvid_path', type=str, default='data/right.mp4', help='right video path')
    parser.add_argument('--lvid_path', type=str, default='data/left.mp4', help='left video path')
    opt = parser.parse_args()
    return opt
    
def load_caps(vid_path, start_time):
    capR = cv2.VideoCapture(vid_path)
    capR.set(cv2.CAP_PROP_POS_FRAMES, start_time * 30)
    return capR

def inference_(frame, session, new_shape, conf_thres):
    ori_images = [frame.copy()]
    resized_image, ratio, dwdh = letterbox(frame, new_shape=new_shape, auto=False)
    input_tensor = preprocess(resized_image)
    outputs = onnx_inference(session, input_tensor)
    pred_output, box_x = post_process(outputs, ori_images, ratio, dwdh, conf_thres)
    return pred_output, box_x
    

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
    #c = 1
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
            right_output, RboxW = inference_(Rstack[-1], session, new_shape, conf_thres)
            left_output, LboxW = inference_(Lstack[-1], session, new_shape, conf_thres)
            frames = np.concatenate((right_output[0], left_output[0]), axis=1)
            Rstack=[]
            Lstack=[]
            if RboxW >0 and LboxW > 0:
                disparity = abs(RboxW-LboxW)
                if disparity <= max_disparity and disparity > min_disparity:
                    h, w = frames.shape[:2]
                    x0, distance, angle, deg = prams_calcurator(disparity, x_pos=RboxW, width=w)
                    texts = 'x:{}, distance(z):{}, disparity:{}, angle : {}'.format(x0, distance, disparity, angle)
                    cv2.putText(frames, texts, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, [225, 255, 255],thickness=2)
            cv2.imshow("Detected Objects", frames)
            #cv2.imwrite('results/frame_{}.png'.format(c), frames)
            #c +=1
        if cv2.waitKey(30) == 27:
            break
    capR.release()
    capL.release()
    
if __name__ == '__main__':
    opt = get_parser()
    capture_process = multiprocessing.Process(target=video_inference, args=(opt,))
    capture_process.start()
   
