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
<img src="https://user-images.githubusercontent.com/48679574/210753162-1e912d47-b09e-46d5-a024-1ade37320e94.png" width="500" height="400"/>

## image
adjust and calibrate parameter by single image 

```sh
python3 main.py --image
```

<img src="https://user-images.githubusercontent.com/48679574/210753196-0752cee8-d34e-466d-8a8f-34e33311cceb.gif" width="500" height="200"/>


# Update Distance and Disparity Formula

・<b>Disparity formula</b> and <b>camera size</b>：

<img src="https://user-images.githubusercontent.com/48679574/208103502-10d83963-b34c-4268-9e89-c1109f7bf2bb.png" width="400" height="300"/><img src="https://user-images.githubusercontent.com/48679574/208103490-39835a32-649e-4cf9-adbf-51bb7d3fd85c.png" width="300" height="300"/>



<b>Disparity formula by python</b>
```python
def distance_formula(disparity):
    T=2.6
    f = 0.315
    img_element = 0.0001*2.8
    K = int(T*f/img_element)
    return K/disparity
```

### Relation of Disparity and Distance(Z axis)

<img src="https://user-images.githubusercontent.com/48679574/208106182-219e477f-7608-4fd0-9345-7d29ab568933.jpg" width="400" height="300"/>


# References
- [Stereo Vision: Depth Estimation between object and camera](https://medium.com/analytics-vidhya/distance-estimation-cf2f2fd709d8)
- [Getting real depth from disparity map](https://stackoverflow.com/questions/23039961/getting-real-depth-from-disparity-map)
