import numpy as np
import cv2
from midas.midas.transforms import Resize, NormalizeImage, PrepareForNet
from torchvision.transforms import Compose


def call_transform(model_type="midas_v21_384"):
    # elif model_type == "midas_v21_384":
    net_w, net_h = 384, 384
    resize_mode = "upper_bound"
    keep_aspect_ratio = False
    normalization = NormalizeImage(
            mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
        )
    transform = Compose(
        [
            Resize(
                net_w,
                net_h,
                resize_target=None,
                keep_aspect_ratio=keep_aspect_ratio,
                ensure_multiple_of=32,
                resize_method=resize_mode,
                image_interpolation_method=cv2.INTER_CUBIC,
            ),
            normalization,
            PrepareForNet(),
        ]
    )
    return transform, net_w, net_h
    
  
def midas_onnx_prediction(frame, transform, onnx_model, net_h, net_w):
    img_input = transform({"image": frame})["image"]
    input_name, output_name = onnx_model.get_inputs()[0].name, onnx_model.get_outputs()[0].name
    onnx_output = onnx_model.run([output_name], {input_name: img_input.reshape(1, 3, net_h, net_w).astype(np.float32)})[0]
    return cv2.normalize(onnx_output[0], None, 0, 1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    #return cv2.applyColorMap((depth_frame*255).astype(np.uint8), cv2.COLORMAP_MAGMA)
    

