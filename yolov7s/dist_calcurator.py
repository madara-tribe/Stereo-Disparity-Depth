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
    if d > 30:
        dif = CAM_PARAM.W_SIDEMAXSITA.value/12
    elif d > 20 and d <= 30:
        dif = CAM_PARAM.W_SIDEMAXSITA.value/10
    elif d > 10 and d <= 20:
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
    #dist_diff = dist_ratio(distance)
    #print("dist_diff, x_angle", dist_diff, x_angle)
    return x_angle, y_angle
    
def distance_formula(disparity, w_element):
    B = CAM_PARAM.CAMS_DIST.value
    f = CAM_PARAM.F.value
    d = w_element
    dist = (f/d)*(B/disparity)
    # print('(f*B/d)', f, B, d, (f*B/d))
    return dist
    
def prams_calcurator(disparity, width, height, x, y):
    w_element = CAM_PARAM.ELEMENT.value * (CAM_PARAM.W_ELEMENT.value / width)
    # h_element = CAM_PARAM.ELEMENT.value * (CAM_PARAM.H_ELEMENT.value / height)
    # print("w_element, h_element", w_element, h_element)
    distance = distance_formula(disparity, w_element)
    angleX, angleY = angle_formula(x, y, width, height, distance)
    return np.round(distance, decimals=2), np.round(angleX, decimals=2), np.round(angleY, decimals=2)
 

