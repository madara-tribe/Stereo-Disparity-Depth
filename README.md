# Disparity Calculator for SoftWare (version = PX2.2)

# Abstract

calcurate distance through disparity and object-detection bbox (yolov7).

Its systems has left and light camera on Jetson, and calcurate distance and disarity from video frame with realtime.

<img src="https://user-images.githubusercontent.com/48679574/208080750-93395d41-45a5-434e-91de-5a8a0928e53e.png" width="500" height="300"/>


・[yolov7Tiny_640_640.onnx](https://drive.google.com/file/d/1QHrRELI8nPjyryiBhyCVEnSk8y8_ziYG/view?usp=sharing)


# Disparity and bbox moment

relations of Disparity and bbox moment with right and left images

<img src="https://user-images.githubusercontent.com/48679574/213966828-29a7f9e2-42f8-4d24-a01f-b439ba581de0.gif" width="500" height="400"/>


# Inference

## video on PyQt

adjust and calibrate parameter by video
```sh
python3 main.py --vid
```

## image
adjust and calibrate parameter by single image 

```sh
python3 main.py --image
```
![スクリーンショット 2024-05-20 13 41 39]()
<img src="https://github.com/madara-tribe/SW-onnx-DisparityCalculator-PX2.0/assets/48679574/4b7f6827-7ed4-4bd6-9b55-3790dfdbc0cb" width="500" height="200"/>


# Update Distance and Disparity Formula

・<b>Disparity formula</b> and <b>camera size</b>：

<img src="https://user-images.githubusercontent.com/48679574/208103502-10d83963-b34c-4268-9e89-c1109f7bf2bb.png" width="400" height="300"/><img src="https://user-images.githubusercontent.com/48679574/208103490-39835a32-649e-4cf9-adbf-51bb7d3fd85c.png" width="300" height="300"/>



<b>Disparity formula by python</b>
```python
class CAM_PARAM(Enum):
    W_ELEMENT = 3280
    H_ELEMENT = 2464
    F = 0.315 # [cm]
    CMS = 1/4 # 8MP, h:1.12 μm, w:1.12μm
    CAMS_DIST = 2.6 # [cm]
    ELEMENT = 0.000112 # [cm]

def distance_formula(disparity, w_element):
    B = CAM_PARAM.CAMS_DIST.value
    f = CAM_PARAM.F.value
    d = w_element
    dist = (f/d)*(B/disparity)
    return dist
```

### Relation of Disparity and Distance(Z axis)

<img src="https://user-images.githubusercontent.com/48679574/208106182-219e477f-7608-4fd0-9345-7d29ab568933.jpg" width="400" height="300"/>


# References
- [Stereo Vision: Depth Estimation between object and camera](https://medium.com/analytics-vidhya/distance-estimation-cf2f2fd709d8)
- [Getting real depth from disparity map](https://stackoverflow.com/questions/23039961/getting-real-depth-from-disparity-map)
