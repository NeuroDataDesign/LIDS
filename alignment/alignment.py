import numpy as np
from matplotlib import pyplot as plt
import cv2

from match_features import *
from detect_features import *
from compute_affine_xform import *
from compute_proj_xform import *

def detect(im1, im2, output, window_size=17, min_ncc=0.7):
    """
    Computes features and matches them using normalized cross correlation (ncc)
    Input:
    im1 (np.array): input image 1. RGB image expected.
    im2 (np.array): input image 2. RGB image expected.
    output (string): desired name of output image.
    window_size (int): size of ncc window.
    min_ncc (float between 0 and 1): minimum ncc required to count as a marriage.
    """

    im1_features = detect_features(im1)
    im2_features = detect_features(im2)

    #uses custom match_features with window size, ncc parameters.
    #Can be replaced with
    #matches = match_features(im1_features, im2_features, im1, im2)
    #for generic behavior (with worse performance)
    matches = match_features_params(im1_features, im2_features, im1, im2, window_size, min_ncc)

    im1_ = im1.copy()
    im2_ = im2.copy()

    #display features
    for (a, b) in im1_features:
        if a < im1.shape[0] and a >= 0 and b < im1.shape[1] and b >= 0:
            cv2.circle(im1_, (b, a), 5, (0, 0, 255), -1)

    for (a, b) in im2_features:
        if a < im2.shape[0] and a >= 0 and b < im2.shape[1] and b >= 0:
            cv2.circle(im2_, (b, a), 5, (0, 0, 255), -1)

    w1, h1 = im1.shape[0], im1.shape[1]
    w2, h2 = im2.shape[0], im2.shape[1]
    max_w = max(w1, w2)
    max_h = max(h1, h2)
    pad1 = np.pad(im1_, ((0, max_w-w1), (0, max_h-h1), (0,0)), "constant")
    pad2 = np.pad(im2_, ((0, max_w-w2), (0, max_h-h2), (0,0)), "constant")

    #display matches
    im_sbs = np.concatenate((pad1, pad2), axis=1)
    for (i,j) in matches:
        x1, y1 = im1_features[i]
        pt1 = (y1, x1)
        x2, y2 = im2_features[j]
        pt2 = (y2+im1_.shape[1], x2)
        cv2.line(im_sbs, pt1, pt2, (0, 255, 0), 2)

    print('saving feature detection and matches as: ' + output)
    cv2.imwrite(output,im_sbs)

def warp(image1, image2, sbs_out, stack_out, window_size = 17, min_ncc = 0.7):
    """
    Computes features and matches, then computes affine transform between image1 and image2.
    Warps image 1 using transform and overlays on top of image2 to confirm transform.

    Input:
    image1 (np.array): input image 1. RGB image expected.
    image2 (np.array): input image 2. RGB image expected.
    sbs_out (string): desired name of side-by-side output image.
    stack_out (string): desired name of stacked output image.
    window_size (int): size of ncc window.
    min_ncc (float between 0 and 1): minimum ncc required to count as a marriage.
    """
    w1, h1 = image1.shape[0], image1.shape[1]
    w2, h2 = image2.shape[0], image2.shape[1]
    max_w = max(w1, w2)
    max_h = max(h1, h2)
    image1 = np.pad(image1, ((0, max_w-w1), (0, max_h-h1), (0,0)), "constant")
    image2 = np.pad(image2, ((0, max_w-w2), (0, max_h-h2), (0,0)), "constant")

    im1_features = detect_features(image1)
    im2_features = detect_features(image2)

    matches = match_features_params(im1_features, im2_features, image1, image2, window_size=window_size, min_ncc=min_ncc)

    affine = compute_affine_xform(matches, im1_features, im2_features, image1, image2, output=sbs_out)
    print('saving side-by-side image as: ' + sbs_out)

    warp_img1 = cv2.warpAffine(image1, affine[:2], image1.shape[0:2][::-1])
    stack = warp_img1/2 + image2/2

    print('saving stacked image as: ' + stack_out)
    cv2.imwrite(stack_out, stack)


def main():
    bikes1 = cv2.imread('input/bikes1.png', 1)
    bikes2 = cv2.imread('input/bikes2.png', 1)
    bikes3 = cv2.imread('input/bikes3.png', 1)

    print('bikes1, bikes2')
    detect(bikes1, bikes2, './output/bikes12features.png')
    warp(bikes1, bikes2, './output/bikes12sbs.png', './output/bikes12stack.png')

    print('\nbikes1, bikes3')
    detect(bikes1, bikes3, './output/bikes13features.png')
    warp(bikes1, bikes3, './output/bikes13sbs.png', './output/bikes13stack.png')

if __name__ == "__main__":
    main()
