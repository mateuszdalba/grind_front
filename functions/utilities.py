import numpy as np
import cv2

def calculate_angle(a,b,c):
    a = np.array(a) #First
    b = np.array(b) #Mid
    c = np.array(c) #End
    
    radians = np.arctan2(c[1] - b[1], c[0]-b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360-angle
        
    return angle

def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h,w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = width/float(w)
        dim = (int(w*r),height)
    else:
        r = width/float(w)
        dim = width, int(h*r)

    # Resize image
    resized = cv2.resize(image,dim,interpolation=inter)
    return resized