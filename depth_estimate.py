import argparse
import time
import sys
import cv2
import numpy as np
import onnxruntime
from yolov7s.common import obdetect_inference
from midas.midas_utils import call_transform, midas_onnx_prediction


def get_cap(opt):
    cap = cv2.VideoCapture(opt.vid_path)
    if not cap.isOpened():
        print('can not open video')
        exit()
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = float(cap.get(cv2.CAP_PROP_FPS))  # FPS
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_frame = cv2.VideoWriter(opt.output_file+"_onnx.mp4", fourcc, fps, (frame_width, frame_height), isColor=False)
    return cap, out_frame, frame_width, frame_height


def qt6_onnx_prepare(opt):
    cuda = False if opt.cpu=='True' else True
    providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'] if cuda else ['CPUExecutionProvider']
    session = onnxruntime.InferenceSession(opt.yolov7_onnx_path, providers=providers)
    IN_IMAGE_H = session.get_inputs()[0].shape[2]
    IN_IMAGE_W = session.get_inputs()[0].shape[3]
    new_shape = (IN_IMAGE_W, IN_IMAGE_H)
    
    # midas
    midas_onnx_model = onnxruntime.InferenceSession(opt.midas_onnx_path)
    return session, new_shape, midas_onnx_model
    
    
def precise_dist(ob_output, px, py, title="Depth in unit: "):
    cv2.putText(ob_output, title + str(5)+'[M]', (px, py-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
    return ob_output
    
def main(opt):
    # obdetect
    conf_thres = opt.conf_thres
    cuda = False if opt.cpu=='True' else True
    providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'] if cuda else ['CPUExecutionProvider']
    session = onnxruntime.InferenceSession(opt.yolov7_onnx_path, providers=providers)
    IN_IMAGE_H = session.get_inputs()[0].shape[2]
    IN_IMAGE_W = session.get_inputs()[0].shape[3]
    new_shape = (IN_IMAGE_W, IN_IMAGE_H)
    
    # midas
    transform, net_h, net_w = call_transform()
    midas_onnx_model = onnxruntime.InferenceSession(opt.midas_onnx_path)
        
    cap, out_format, frame_width, frame_height = get_cap(opt)
    cv2.namedWindow("Detected Objects", cv2.WINDOW_NORMAL)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        start = time.time()
        # midas inference
        depth_midas = midas_onnx_prediction(frame, transform, midas_onnx_model, net_h, net_w)
        depth_midas = cv2.resize(depth_midas, (frame_width, frame_height))
        
        # object detectioon inference
        ob_output, mid_x, mid_y = obdetect_inference(frame, depth_midas, session, new_shape, conf_thres)
        print(time.time()-start)
        
        # Create a spline object using the output_norm array
        ob_output = precise_dist(ob_output, depth_midas, mid_x=866, mid_y=400, px=866, py=400, title="Difine: ")
        cv2.imshow("Detected Objects", ob_output)
        if cv2.waitKey(30) == 27:
            break
    out_format.release()
    cap.release()
    
    
"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--yolov7_onnx_path', type=str, default='weights/yolov7Tiny_640_640.onnx', help='image path')
    parser.add_argument('--midas_onnx_path', type=str, default='weights/model-f6b98070.onnx', help='onnx midas weight model')
    parser.add_argument('--cpu', type=str, default='True', help='if cpu is None, use CUDA')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='conf threshold for NMS or postprocess')
    parser.add_argument('--vid_path', type=str, default='data/outdriving.mov', help='right video path')
    parser.add_argument('-o', '--output_file', type=str, default='data/movie', help='movie output path')
    parser.add_argument('-s', '--show', action='store_true', help='prepare test data')
    opt = parser.parse_args()
    try:
        main(opt)
    except KeyboardInterrupt:
        sys.exit(1)
        raise
"""
