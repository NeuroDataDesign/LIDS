import cv2
import numpy as np
import matplotlib.pyplot as plt
import random

def compute_affine_xform(matches,features1,features2,image1,image2, output='output.png'):
    """
    Computer Vision 600.461/661 Assignment 2
    Args:
        matches (list of tuples): list of index pairs of possible matches. For example, if the 4-th feature in feature_coords1 and the 0-th feature
                                  in feature_coords2 are determined to be matches, the list should contain (4,0).
        features1 (list of tuples) : list of feature coordinates corresponding to image1
        features2 (list of tuples) : list of feature coordinates corresponding to image2
        image1 (numpy.ndarray): The input image corresponding to features_coords1
        image2 (numpy.ndarray): The input image corresponding to features_coords2
        output (string): Optional argument for output filename of image. Defaults to output.png
    Returns:
        proj_xform (numpy.ndarray): a 3x3 Projective transformation matrix between the two images, computed using the matches.
    """
    
    affine_xform = np.zeros((3,3))

    #choose number of matches
    selection = 3
    err = 5
    
    match_inds = [i for i in range(len(matches))] 
    matched = [] #remember combinations 

    N = 20000 # repeat algorithm N times
    max_inliers = -1
    best_inliers = []
    
    np.random.seed(80)
    

    for i in range(N):
        #randomly choose selection=3 matches
        random.shuffle(match_inds)
        sample = match_inds[:selection]
        
        #populate A, B
        A = []
        b = []
        for idx in sample:
            f1, f2 = matches[idx]
            y1, x1 = features1[f1]
            y2, x2 = features2[f2]
            A.extend([[x1, y1, 1, 0, 0, 0],[0, 0, 0, x1, y1, 1]])
            b.extend([[x2], [y2]])

        #calculate least squares solution
        A = np.array(A).astype('float64')
        b = np.array(b).astype('float64')
        try:
            pinv_A = np.linalg.inv(A.T.dot(A)).dot(A.T)
        except np.linalg.linalg.LinAlgError:
            #if singular... skip. 
            #Somehow, this is never encountered when I was testing in Jupyter Notebook
            #but I encountered it in the command line.
            #I ran it by Yotam and he suggested this workaround.
            continue
            
        y = pinv_A.dot(b) #y = (A^TA)^-1 A^T b
        y = np.reshape(y, (2,3)) #fix dimensions
        y = np.concatenate((y, [[0, 0, 1]]), axis=0) #add last row
        
        curr_inliers = []
        
        for match in matches:
            (i,j) = match
            y1, x1 = features1[i]
            y1_predict, x1_predict = features2[j]
            
            rx = (y[0,0]*x1+y[0,1]*y1+y[0,2]-x1_predict)
            ry = (y[1,0]*x1+y[1,1]*y1+y[1,2]-y1_predict)
#             print(i,j,rx*rx+ry*ry)
            if np.sqrt(rx*rx + ry*ry) < err:
                curr_inliers.append((i,j))
                
        if len(curr_inliers) > max_inliers:
            max_inliers = len(curr_inliers)
            best_inliers = curr_inliers
            affine_xform = y
    
    #padding image to deal with different sized images
    w1, h1 = image1.shape[0], image1.shape[1]
    w2, h2 = image2.shape[0], image2.shape[1]        
    max_w = max(w1, w2)
    max_h = max(h1, h2)
    pad1 = np.pad(image1, ((0, max_w-w1), (0, max_h-h1), (0,0)), "constant")
    pad2 = np.pad(image2, ((0, max_w-w2), (0, max_h-h2), (0,0)), "constant")
    
    #draw inliers and outliers to relative to best inlier set.
    im_sbs = np.concatenate((pad1, pad2), axis=1)
    for match in matches:
        (i,j) = match
        x1, y1 = features1[i]
        pt1 = (y1, x1)
        cv2.circle(im_sbs, pt1, 5, (0, 0, 255), -1)
        x2, y2 = features2[j]
        pt2 = (y2+image1.shape[1], x2)
        cv2.circle(im_sbs, pt2, 5, (0, 0, 255), -1)
        if match in best_inliers:
            cv2.line(im_sbs, pt1, pt2, (0, 255, 0), 2)
        else:
            cv2.line(im_sbs, pt1, pt2, (0, 0, 255), 2)  
    
    #save the image.
    cv2.imwrite(output, im_sbs)
    
    return affine_xform
