# Disparity Calculator for SoftWare (version = PX2.2)

・[version=PX2.0](https://github.com/madara-tribe/SW-onnx-DisparityCalculator-PX2.0/tree/px2.0)


calcurate distance through disparity and object-detection bbox (yolov7).

Its systems has left and light camera on Jetson, and calcurate distance and disarity from video frame with realtime.

<img src="https://user-images.githubusercontent.com/48679574/208080750-93395d41-45a5-434e-91de-5a8a0928e53e.png" width="500" height="300"/>


## Relation of Disparity and Distance(Z axis)

<img src="https://user-images.githubusercontent.com/48679574/208106182-219e477f-7608-4fd0-9345-7d29ab568933.jpg" width="300" height="200"/>



# Inference

### PyQt

### image
adjust and calibrate parameter by single image 

<img src="https://github.com/madara-tribe/SW-onnx-DisparityCalculator-PX2.2/assets/48679574/cdb83bdf-4120-4dd6-9e42-88d653e4c856" width="300" height="200"/>

```sh
python3 main.py --img
```
### video
test by movie 

```sh
python3 main.py --vid
```

# Update Distance and Disparity Formula

・[Focal Lenth mm to pixel](https://answers.opencv.org/question/17076/conversion-focal-distance-from-mm-to-pixels/)


<b>Disparity formula by python</b>
```python
# focal lenth m to px
fpx = forcal_lenth_px = (hyp['FOCAL_LENTH'] * width)/hyp['W_PIXEL_LENTH'] # [px]

# calcurate distance
def distance_formula(disparity, fpx, hyp):
    B = hyp['CAM_BASELINE'] # [mm]
    dist = (fpx*B)/disparity # [mm]
    return dist

# calcurate real x, y, z cordinate
def real_cordinate(cx, cy, x, y, fpx, z):
    real_x = (abs(x-cx)*z) / fpx
    real_y = (abs(y-cy)*z) / fpx
    print("real_x, (abs(x-cx)*z), real_y, (abs(y-cy)*z)", real_x, (abs(x-cx)*z), real_y, (abs(y-cy)*z))
    return real_x, real_y
```



# References
- [Stereo Vision: Depth Estimation between object and camera](https://medium.com/analytics-vidhya/distance-estimation-cf2f2fd709d8)
- [Getting real depth from disparity map](https://stackoverflow.com/questions/23039961/getting-real-depth-from-disparity-map)
- [optical camera technical information](https://www.shodensha-inc.co.jp/solution/)
