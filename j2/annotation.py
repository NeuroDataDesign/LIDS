import numpy as np
import pandas as pd
from skimage.io import imsave
from util import get_radius, create_oval_mask


def create_annotation_volume(csv_path, img_shape, fname):
    """
    Creates an annotation image using Overlay Elements
    from ROI Manager in FIJI. Overlay Elements are created
    from List option in ROI Manager.

    Parameters
    ----------
    csv_path : str
        Path to the csv output from ROI Manager
    img_shape : tuple
        Output image shape in (z, y, x) format
    fname : str
        Name of output image
    """
    df = pd.read_csv(csv_path, index_col='Index')

    out = np.empty(img_shape, dtype=np.int)

    for row in df.iterrows():
        width = row[1]['Width']
        height = row[1]['Height']
        x, y, z = row[1]['X'], row[1]['Y'], row[1]['Z'] - 1
        index = row[0] + 1  #ROI index starts at 0, but it cannot be 0 in output

        mask = create_oval_mask(width, height) * index

        w_radius = get_radius(width)
        h_radius = get_radius(height)

        ridx, cidx = np.where(mask)
        absidxR = (y + ridx - w_radius).astype(np.int)
        absidxC = (x + cidx - h_radius).astype(np.int)

        valid_mask = (absidxR >= 0) & (absidxR < out.shape[2]) & \
                     (absidxC >= 0) & (absidxC < out.shape[1])

        out[z, absidxR[valid_mask], absidxC[valid_mask]] = index

    if '.tif' in fname:
        io.imsave(fname, out.astype(np.uint16))
    else:
        io.imsave(fname + '.tiff', out.astype(np.uint16))


if __name__ == '__main__':
    csv_path = '../data/Overlay Elements.csv'
    img_shape = (16, 359, 359)
    fname = 'annotation.tiff'

    create_annotation_volume(csv_path, img_shape, fname)
