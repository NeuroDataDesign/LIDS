import matplotlib.pyplot as plt
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

    y, x = np.ogrid[-h_radius:h_radius + 1, -w_radius:w_radius + 1]

    out = (x**2 / (width / 2)**2) + (y**2 / (height / 2)**2) <= 1

    return out


def calculate_stats(overlap_dict):
    """
    Calculates precision, recall and f1 measures.
    """
    arr = np.array(overlap_dict['gtPerPrediction'])
    tp = np.sum([arr >= 1])
    fp = np.sum([arr == 0])

    arr = np.array(overlap_dict['predictionPerGt'])
    fn = np.sum(np.ones_like(arr)) - tp

    prec = tp / (tp + fp)
    rec = tp / (tp + fn)
    f1 = (2 * prec * rec) / (prec + rec)

    return prec, rec, f1


def remove_labels(img, threshold):
    """
    Remove labels with number of voxels that is below threshold.

    Parameters
    ----------
    img : 3d-array
    threshold : int
        Cutoff value. Must be greater than 0.
    """
    assert threshold > 0, "Cutoff value must be greater than 0"
    assert type(threshold) == int, "Cutoff value must be an integer"

    out = np.copy(img)

    bins = np.bincount(out.ravel())
    idx = np.where(bins <= threshold)[0]

    for i in idx:
        out[out == i] = 0

    return out


def overlay_images(img_1, img_2):
    """
    Creates an overlap image using two image volumes.
    """
    assert img_1.shape == img_2.shape, "The two image volumes must have same dimensions."

    mask_img_1 = np.stack([z > 0 for z in img_1])
    mask_img_2 = np.stack([z > 0 for z in img_2])

    rgb_img = np.moveaxis(
        np.stack([mask_img_1, mask_img_2,
                  np.zeros_like(mask_img_1)]), 0, -1)
    rgb_img = rgb_img.astype(float)

    return rgb_img
