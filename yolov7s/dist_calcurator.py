import numpy as np
from enum import Enum

class DistConst(Enum):
    CriteriaX = 866
    CriteriaY = 400
    RealLenth = 5 # m
    
def calcurate_distance(ori_images, depth_midas, mid_x, mid_y):
    #oriH, oriW, _ = ori_images.shape
    # print("oriH, oriW",oriH, oriW) 500 1732
    mid_z = depth_midas[int(mid_y)][int(mid_x)]
    cri_z = depth_midas[DistConst.CriteriaY.value][DistConst.CriteriaX.value]
    target_dist = (DistConst.RealLenth.value * mid_z) / cri_z
    return np.round(target_dist, decimals=2)
