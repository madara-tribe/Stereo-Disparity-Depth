# Disparity Calculator for SoftWare(SW)

# Abstract

calcurate distance through disparity and object-detection bbox (yolov7).

Its systems has left and light camera on Jetson, and calcurate video frame with realtime.

<img src="https://user-images.githubusercontent.com/48679574/208080750-93395d41-45a5-434e-91de-5a8a0928e53e.png" width="600" height="400"/>

# Inference

## video on PyQt
```sh
python3 main.py --qt
```
<img src="https://user-images.githubusercontent.com/48679574/208105192-51a3e2a4-e6c8-47c9-93fe-98dacdb18021.png" width="400" height="300"/>


## image
```sh
python3 main.py --image
```
## video
```sh
python3 main.py --vid
```

<img src="https://user-images.githubusercontent.com/48679574/208105250-9ff22852-5824-46fd-b8f5-6b3bde634f43.gif" width="400" height="300"/>


# Formula

・<b>Disparity formula</b> and <b>camera size</b>：

<img src="https://user-images.githubusercontent.com/48679574/208103502-10d83963-b34c-4268-9e89-c1109f7bf2bb.png" width="400" height="300"/><img src="https://user-images.githubusercontent.com/48679574/208103490-39835a32-649e-4cf9-adbf-51bb7d3fd85c.png" width="300" height="300"/>



<b>Disparity formula by python</b>
```python
def disranse_formula(disparity):
    T=2.6
    f = 0.315
    img_element = 0.0001*2.8
    K = int(T*f/img_element)
    return K/disparity
```

## Relation of Disparity and Distance(Z axis)


# References
- [ONNX-YOLOv7-Object-Detection](https://github.com/ibaiGorordo/ONNX-YOLOv7-Object-Detection)




