# Simulate Jetson ONNX 3dDepth Calcurator advanced

Use onnx yolov7-tiny and midas-onnx model to calcurate 3d depth distance with camera on Qt6.

This is the system that simulates to estimate 3d distances of the objects on images captured by cameras。

Used model is
- midas (depth calcuration)
- yolov7 (object detection)

previous classic style system is [here](https://github.com/madara-tribe/Qt6-classic-Depth-Calcurator). 

This time system get more advanced and presize calcuration 

<b>avarage inference time (midas + yolov7) on CPU</b>
```txt
760.16 [ms]
```


# area to estimate distance in this movie 

you can not adapt this calcuration system to <b>「Out of area」</b>

<img src="https://github.com/madara-tribe/Qt6-MiDaS-depth-calculater/assets/48679574/4d0b30f1-246a-4e44-93f1-f536951ccbde" width="600px" height="300px">



# 3D distance calcurate formula 

```math
\begin{array}
\bigl({c_x}={criteria_x}\hspace{0.5cm}{c_y}={criteria_y}\hspace{0.5cm}{C_d}=CriteriaDistance)\\
\bigl({t_x}={target_x}\hspace{0.5cm}{t_y}={target_y}\hspace{0.5cm}{T_d}=TargetDistance)\\
\bigl(D=DepthMap)
\end{array}
```

```math
DipthRatio = \boldsymbol{D(x,y)} \hspace{2cm}
```

```math
(Formula)\hspace{5cm}{T_d} = \frac{{C_d} \times \boldsymbol{D({t_x},{t_y})}}{\boldsymbol{D({c_x}, {c_y})}}
```

  

# Inference GIF

<img src="https://github.com/madara-tribe/Qt6-MiDaS-depth-calculater/assets/48679574/0143b8eb-464a-4d92-8e27-d37a9bc0ec58" width="600px">

<b>Sample driving movie</b>
- [sample driving movie](https://drive.google.com/file/d/18P0mS9fjMD1nq2tKMzD-u_eXjpjttJ4n/view?usp=sharing)


# References
- [Getting Started with Depth Estimation using MiDaS and Python](https://medium.com/artificialis/getting-started-with-depth-estimation-using-midas-and-python-d0119bfe1159)
