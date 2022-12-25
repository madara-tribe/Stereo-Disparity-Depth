import os
import numpy as np
from enum import Enum

class Formula(Enum):
    T = 2.6
    F = 0.315
    IMG_ELEMENT = 0.00028
    K = 2925
    
def disranse_formula(disparity):
    T=2.6
    f = 0.315
    img_element = 0.0001*2.8
    K = int(T*f/img_element)
    return K/disparity
    
def prams_calcurator(disparity):
    distance = Formula.K.value / disparity   #  disranse_formula(disparity)
    return np.round(distance, decimals=2)
 

