import argparse
import time
import cv2
import numpy as np
import onnxruntime
import multiprocessing
from common import letterbox, preprocess, onnx_inference, post_process


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--onnx_path', type=str, default='yolov7Tiny_640_640.onnx', help='image path')
    parser.add_argument('--cpu', type=str, default='True', help='if cpu is None, use CUDA')
    parser.add_argument('--rvid_path', type=str, default='data/right.mp4', help='right video path')
    parser.add_argument('--lvid_path', type=str, default='data/left.mp4', help='left video path')
    opt = parser.parse_args()
    return opt
    
def load_caps(vid_path, start_time):
    capR = cv2.VideoCapture(vid_path)
    capR.set(cv2.CAP_PROP_POS_FRAMES, start_time * 30)
    return capR

def inference_(frame, session, new_shape):
    ori_images = [frame.copy()]
    resized_image, ratio, dwdh = letterbox(frame, new_shape=new_shape, auto=False)
    input_tensor = preprocess(resized_image)
    outputs = onnx_inference(session, input_tensor)
    pred_output = post_process(outputs, ori_images, ratio, dwdh)
    return pred_output
    

def video_inference(opt):
    onnx_path = opt.onnx_path
    cuda = False if opt.cpu=='True' else True
    start_time = 0
    capR = load_caps(vid_path=opt.rvid_path, start_time=start_time)
    capL = load_caps(vid_path=opt.lvid_path, start_time=start_time)
    providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'] if cuda else ['CPUExecutionProvider']
    session = onnxruntime.InferenceSession(onnx_path, providers=providers)

    IN_IMAGE_H = session.get_inputs()[0].shape[2]
    IN_IMAGE_W = session.get_inputs()[0].shape[3]
    new_shape = (IN_IMAGE_W, IN_IMAGE_H)
    
    cv2.namedWindow("Detected Objects", cv2.WINDOW_NORMAL)
    #c = 1
    while capR.isOpened() and capL.isOpened():
        try:
            retR, frame_right = capR.read()
            retL, frame_left = capL.read()
            if not retR or not retL:
                break
        except Exception as e:
            print(e)
            continue

        # inference each frame
        right_output = inference_(frame_right, session, new_shape)
        left_output = inference_(frame_left, session, new_shape)
        frames = np.concatenate((right_output[0], left_output[0]), axis=1)
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
   
