import os
import numpy as np
from enum import Enum


class DistFormula(Enum):
    T = 2.6
    F = 0.315
    IMG_ELEMENT = 0.00028
    K = 2925
    
class AngleFormula(Enum):
    SerboMaxAngle = 180

def angle_formula(x, y, w):
    angleX = x / (w/AngleFormula.SerboMaxAngle.value)
    angleY = y / (w/AngleFormula.SerboMaxAngle.value)
    return angleX, angleY
    
def distance_formula(disparity):
    T=2.6
    f = 0.315
    img_element = 0.0001*2.8
    K = int(T*f/img_element)
    return K/disparity
    
def prams_calcurator(disparity, width, x, y):
    distance = DistFormula.K.value / disparity   #  disranse_formula(disparity)
    angleX, angleY = angle_formula(x, y, width)
    return np.round(distance, decimals=2), np.round(angleX, decimals=2), np.round(angleY, decimals=2)
 

