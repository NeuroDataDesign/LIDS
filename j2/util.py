import numpy as np
import pandas as pd
import skimage.io as io


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

def main():
    #Overlay Elements from ROI Manager -> List option
    df = pd.read_csv('../data/Overlay Elements.csv', index_col = 'Index')

    out = np.empty((16, 359, 359), dtype=np.int)

    for row in df.iterrows():
        width = row[1]['Width']
        height = row[1]['Height']
        x, y, z = row[1]['X'], row[1]['Y'], row[1]['Z'] - 1
        index = row[0] + 1 # ROI index starts at 0, but it cannot be 0 in output

        mask = create_oval_mask(width, height) * index

        w_radius = get_radius(width)
        h_radius = get_radius(height)

        ridx, cidx = np.where(mask)
        absidxR = (y + ridx - w_radius).astype(np.int)
        absidxC = (x + cidx - h_radius).astype(np.int)
        
        valid_mask = (absidxR >= 0) & (absidxR < out.shape[2]) & \
                     (absidxC >= 0) & (absidxC < out.shape[1])
        
        out[z, absidxR[valid_mask], absidxC[valid_mask]] = index
    
    io.imsave('../data/annotation.tiff', out.astype(np.uint16))

if __name__ == '__main__':
    main()