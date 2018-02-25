import numpy as np
import cv2

def match_features(feature_coords1, feature_coords2, image1, image2):
    """
    Computer Vision 600.461/661 Assignment 2
    Args:
        feature_coords1 (list of tuples): list of (row,col) tuple feature coordinates from image1
        feature_coords2 (list of tuples): list of (row,col) tuple feature coordinates from image2
        image1 (numpy.ndarray): The input image corresponding to features_coords1
        image2 (numpy.ndarray): The input image corresponding to features_coords2
    Returns:
        matches (list of tuples): list of index pairs of possible matches. 
        For example, if the 4-th feature in feature_coords1 and the 0-th feature
        in feature_coords2 are determined to be matches, the list should contain (4,0).
    """
    #allows window size, ncc threshold to be customizable.
    window_size = 17
    min_ncc = 0.7
    
    matches = match_features_params(feature_coords1, feature_coords2, image1, image2)
    return matches

def match_features_params(feature_coords1, feature_coords2, image1, image2, window_size = 17, min_ncc = 0.7):
    """
    Computer Vision 600.461/661 Assignment 2
    Args:
        feature_coords1 (list of tuples): list of (row,col) tuple feature coordinates from image1
        feature_coords2 (list of tuples): list of (row,col) tuple feature coordinates from image2
        image1 (numpy.ndarray): The input image corresponding to features_coords1 (RGB)
        image2 (numpy.ndarray): The input image corresponding to features_coords2 (RGB)
        window_size (integer): size of the window for ncc comparisons. default = 17
        min_ncc (float between 0 and 1): minimum value of ncc that will be accepted as a match. default = 0.7
    Returns:
        matches (list of tuples): list of index pairs of possible matches. 
        For example, if the 4-th feature in feature_coords1 and the 0-th feature
        in feature_coords2 are determined to be matches, the list should contain (4,0).
    """
    
    #helper function to compute ncc between patches around features
    def ncc(window_size, feature1, feature2, image1, image2):
        i1,j1 = feature1
        i2,j2 = feature2
        
        delta = window_size/2
        patch1 = image1[i1-delta:i1+delta+1, j1-delta:j1+delta+1]
        patch2 = image2[i2-delta:i2+delta+1, j2-delta:j2+delta+1]
        #If the patch is too close to the edge
        if patch1.shape != (window_size, window_size) or patch2.shape != (window_size, window_size):
            return None
        else:
            normpatch1 = (patch1 - np.mean(patch1))/np.std(patch1)
            normpatch2 = (patch2 - np.mean(patch2))/np.std(patch2)
            ncc_window = np.multiply(normpatch1, normpatch2)
            return ncc_window.mean()

    #convert image to RGB
    gray_im1 = cv2.cvtColor(image1, cv2.COLOR_RGB2GRAY)
    gray_im2 = cv2.cvtColor(image2, cv2.COLOR_RGB2GRAY)
    
    #1->2 matching    
    match1to2 = list()
    for i in range(len(feature_coords1)):
        nccvals = np.array(list())
        for j in range(len(feature_coords2)):
            n0 = ncc(window_size, feature_coords1[i], feature_coords2[j], gray_im1, gray_im2)
            if n0 is None:
                nccvals = np.append(nccvals, np.NINF)
            else:
                nccvals = np.append(nccvals, n0)
        if np.max(nccvals) > min_ncc:
            match1to2.append(np.argmax(nccvals))
        else:
            match1to2.append(-1)
    #2->1 matching
    match2to1 = list()
    for j in range(len(feature_coords2)):
        nccvals = np.array(list())
        for i in range(len(feature_coords1)):
            n0 = ncc(window_size, feature_coords1[i], feature_coords2[j], gray_im1, gray_im2)
            if n0 is None:
                nccvals = np.append(nccvals, np.NINF)
            else:
                nccvals = np.append(nccvals, n0)
        if np.max(nccvals) > min_ncc:
            match2to1.append(np.argmax(nccvals))
        else:
            match2to1.append(-1)
    
    matches = list()
    for i in range(len(feature_coords1)):
        for j in range(len(feature_coords2)):
                if match1to2[i] == j and match2to1[j] == i:
                    matches.append((i,j))
                    
    return matches