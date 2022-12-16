import time
import cv2
import onnxruntime

from .common import letterbox, preprocess, onnx_inference, post_process


def image_inference(opt):
    cuda = False if opt.cpu=='True' else True
    onnx_path = opt.onnx_path
    conf_thres = opt.conf_thres
    img = cv2.imread(opt.img_path)
    h, w, c = img.shape
    ori_images = [img.copy()]
    providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'] if cuda else ['CPUExecutionProvider']
    session = onnxruntime.InferenceSession(onnx_path, providers=providers)

    IN_IMAGE_H = session.get_inputs()[0].shape[2]
    IN_IMAGE_W = session.get_inputs()[0].shape[3]
    new_shape = (IN_IMAGE_W, IN_IMAGE_H)
    # preprocess input
    resized_image, ratio, dwdh = letterbox(img, new_shape=new_shape, auto=False)
    input_tensor = preprocess(resized_image)
    print('input_tensor shape', input_tensor.shape)
    
    print("start inference", cuda)
    start = time.perf_counter()
    outputs = onnx_inference(session, input_tensor)
    pred_output = post_process(outputs, ori_images, ratio, dwdh, conf_thres)
    if isinstance(pred_output, list) or isinstance(pred_output, tuple):
         pred_output = np.array(pred_output[0])
    if len(pred_output.shape)==4:
        pred_output = pred_output.reshape(h, w, c)
    print(f"Inference time: {(time.perf_counter() - start)*1000:.2f} ms")
    print("output shape is ", pred_output.shape)
    cv2.imwrite("output.png", pred_output)
    
