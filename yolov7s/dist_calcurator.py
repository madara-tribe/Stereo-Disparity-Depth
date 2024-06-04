import numpy as np
from enum import Enum


class CAM_PARAM(Enum):
    W_ELEMENT = 3280
    H_ELEMENT = 2464
    F = 0.315 # [cm]
    CMS = 1/4 # 8MP, h:1.12 μm, w:1.12μm
    CAMS_DIST = 2.6 # [cm]
    ELEMENT = 0.000112 # [cm]
    W_SIDEMAXSITA = 50
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
    
def angle_formula(x, y, width, height, distance):
    ox, oy = abs(x-int(width/2)), abs(y-int(height/2))
    width_pixel_angle = CAM_PARAM.W_SIDEMAXSITA.value/int(width/2)
    height_pixel_angle = CAM_PARAM.H_SIDEMAXSITA.value/int(height/2)
    # x angle
    if x < int(width/2):
        x_angle = 40 + (x * width_pixel_angle)
    elif x >= int(width/2):
        x_angle = 90 + abs(x-int(width/2)) * width_pixel_angle
    # y angle
    if y < int(height/2):
        y_angle = y * height_pixel_angle
    elif y >= int(height/2):
        y_angle = 20 + abs(y-int(height/2)) * height_pixel_angle

    # dist
    dist_diff = dist_ratio(distance)
    #print("dist_diff, x_angle", dist_diff, x_angle)
    return x_angle-dist_diff, y_angle
    
def distance_formula(disparity, w_element, hyp):
    B = hyp['CAM_BASELINE'] # [cm]
    f = hyp['FOCAL_LENTH'] # [cm]
    d = w_element # [cm/px]
    dist = (f/d)*(B/disparity) # [cm]
    print('(f*B/d)', f, B, d, (f*B/d))
    return dist
    
def prams_calcurator(hyp, disparity, width, height, x, y):
    w_element = hyp['W_PER_PIXEL_ELEMENT'] * (hyp['W_RESOLUTION'] / width) # [cm/px]
    # h_element = hyp['H_PER_PIXEL_ELEMENT'] * (hyp['H_RESOLUTION'] / height) # [cm/px]
    # print("w_element, h_element", w_element, h_element)
    distance = distance_formula(disparity, w_element, hyp)
    angleX, angleY = angle_formula(x, y, width, height, distance)
    return disparity, np.round(distance, decimals=2), np.round(angleX, decimals=2), np.round(angleY, decimals=2)
 

