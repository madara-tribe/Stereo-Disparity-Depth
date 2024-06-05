import numpy as np
from enum import Enum


class CAM_PARAM(Enum):
    W_ELEMENT = 3280
    H_ELEMENT = 2464
    F = 0.315 # [cm]
    CMS = 1/4 # 8MP, h:1.12 μm, w:1.12μm
    CAMS_DIST = 2.6 # [cm]
    ELEMENT = 0.000112 # [cm]
    W_SIDEMAXSITA = 100
    H_SIDEMAXSITA = 20
 
def dist_ratio(d):
    if d > 50:
        dif = CAM_PARAM.W_SIDEMAXSITA.value/12
    elif d > 40 and d <= 50:
        dif = CAM_PARAM.W_SIDEMAXSITA.value/10
    elif d > 30 and d <= 40:
        dif = CAM_PARAM.W_SIDEMAXSITA.value/8
    else:
        dif = 0
    return dif
    
def angle_formula(x, y, w_per_angle, h_per_angle, distance):
    width_angle = w_per_angle * x
    height_angle = h_per_angle * y

    # dist
    dist_diff = dist_ratio(distance)
    #print("dist_diff, x_angle", dist_diff, x_angle)
    return width_angle, height_angle
    
def distance_formula(disparity, w_element, hyp):
    B = hyp['CAM_BASELINE'] # [cm]
    f = hyp['FOCAL_LENTH'] # [cm]
    d = w_element # [cm/px]
    dist = (f/d)*(B/disparity) # [cm]
    print('(f*B/d)', f, B, d, (f*B/d))
    return dist
    
def prams_calcurator(hyp, disparity, width, height, x, y):
    w_per_angle = (hyp['W_RESOLUTION'] / width) * (CAM_PARAM.W_SIDEMAXSITA.value/ width) # [θ]
    h_per_angle =  (hyp['H_RESOLUTION'] / height) * (CAM_PARAM.H_SIDEMAXSITA.value / height) # [θ]
    # print("w_element, h_element", w_element, h_element)
    distance = distance_formula(disparity, w_element, hyp)
    angleX, angleY = angle_formula(x, y, w_per_angle, h_per_angle, distance)
    return disparity, np.round(distance, decimals=2), np.round(angleX, decimals=2), np.round(angleY, decimals=2)
 

