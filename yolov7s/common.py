import cv2
import random
import numpy as np
from .dist_calcurator import calcurate_distance
TARGET_CANDIDATE_CLS = ['car', 'bus', 'truck']

names = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
         'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
         'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
         'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
         'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
         'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
         'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
         'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
         'hair drier', 'toothbrush']
colors = {name:[random.randint(0, 255) for _ in range(3)] for i,name in enumerate(names)}


def letterbox(im, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleup=True, stride=32):
    # Resize and pad image while meeting stride-multiple constraints
    shape = im.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better val mAP)
        r = min(r, 1.0)

    # Compute padding
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding

    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return im, r, (dw, dh)

def preprocess(img):
    # Scale input pixel values to 0 to 1
    image = np.expand_dims(img.transpose((2, 0, 1)), 0)
    image = np.ascontiguousarray(image)
    return image.astype(np.float32) / 255

def onnx_inference(session, input_tensor):
    output_names = [i.name for i in session.get_outputs()]
    input_names = [i.name for i in session.get_inputs()]
    inp = {input_names[0]:input_tensor}
    outputs = session.run(output_names, inp)[0]
    return outputs

def post_process(outputs, ori_images, ratio, dwdh, conf_thres, depth_midas):
    mid_x, mid_y = 0, 0
    for i, (batch_id, x0, y0, x1, y1, cls_id, score) in enumerate(outputs):
        image = ori_images[int(batch_id)]
        box = np.array([x0,y0,x1,y1])
        box -= np.array(dwdh*2)
        box /= ratio
        box = box.round().astype(np.int32).tolist()
        cls_id = int(cls_id)
        score = round(float(score),3)
        if score < conf_thres:
            continue
        name = names[cls_id]
        if name not in TARGET_CANDIDATE_CLS:
            continue
        color = colors[name]
        name += ' '+str(score)
        mid_x = (box[2:][0]+box[:2][0])/2 # w+x/2
        mid_y = (box[2:][1]+box[:2][1])/2 # h+y/2
        target_dist = calcurate_distance(image, depth_midas, mid_x, mid_y)
        # cv2.rectangle(image, box[:2], box[2:], color, 2)
        cv2.putText(image, str(target_dist)+'M', (box[0], box[1] - 2),cv2.FONT_HERSHEY_SIMPLEX,0.75,[225, 255, 255],thickness=2)
        cv2.circle(image, (int(mid_x), int(mid_y)), 5, (255, 255, 255), thickness=-1)
    return ori_images, mid_x, mid_y


def obdetect_inference(frame, depth_midas, session, new_shape, conf_thres):
    ori_images = [frame.copy()]
    resized_image, ratio, dwdh = letterbox(frame, new_shape=new_shape, auto=False)
    input_tensor = preprocess(resized_image)
    outputs = onnx_inference(session, input_tensor)
    pred_output, coordinate_x, coordinate_y = post_process(outputs, ori_images, ratio, dwdh, conf_thres, depth_midas)
    return pred_output[0], coordinate_x, coordinate_y
