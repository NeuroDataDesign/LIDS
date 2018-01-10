import numpy as np

def get_radius(d):
    if d % 2 != 0:
        r = (d - 1) / 2
    else:
        r = d / 2
    
    return r

def create_oval_mask(width, height):
    w_radius = get_radius(width)
    h_radius = get_radius(height)
    
    y, x = np.ogrid[-h_radius:h_radius + 1,
                    -w_radius:w_radius + 1]
    
    out = (x**2 / (width / 2)**2) + (y**2 / (height / 2)**2) <= 1
    
    return out