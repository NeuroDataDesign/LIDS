import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
from skimage import measure
import numpy as np
import seaborn as sns
import pandas as pd


def overlap(predicted_regions, annotations):
    annotation_per_pred = dict()
    for region in predicted_regions:
        annotation_per_pred[region.centroid] = []
        for idx, row in annotations.iterrows():
            xmin = row['X']
            xmax = row['X'] + row['Width']
            ymin = row['Y']
            ymax = row['Y'] + row['Height']
            if region.centroid[1] <= xmax and region.centroid[1] >= xmin \
                and region.centroid[0] <= ymax and region.centroid[0] >= ymin:
                annotation_per_pred[region.centroid].append((row['X'], row['Y']))

    pred_per_annotation = dict()
    for idx, row in annotations.iterrows():
        pred_per_annotation[(row['X'], row['Y'])] = []
        for region in predicted_regions:
            xmin = row['X']
            xmax = row['X'] + row['Width']
            ymin = row['Y']
            ymax = row['Y'] + row['Height']
            if region.centroid[1] <= xmax and region.centroid[1] >= xmin \
                and region.centroid[0] <= ymax and region.centroid[0] >= ymin:
                pred_per_annotation[(row['X'], row['Y'])].append(region.centroid)

    return {'pred_per_ann': pred_per_annotation, 'ann_per_pred': annotation_per_pred}

def compute_stats(overlap_dict):
    arr = np.array([len(overlap_dict['ann_per_pred'][key]) for key in overlap_dict['ann_per_pred'].keys()])
    tp = np.sum([arr >= 1])
    fp = np.sum([arr == 0])

    arr = np.array([len(overlap_dict['pred_per_ann'][key]) for key in overlap_dict['pred_per_ann'].keys()])
    tn = np.sum([arr >= 1])
    fn = np.sum([arr == 0])

    prec = tp / (tp + fp)
    rec = tp / (tp + fn)
    f1 = (2 * prec * rec) / (prec + rec)

    sensitivity = tp / (tp + fn)
    specificity = tn / (tn + fp)

    return prec, rec, f1, sensitivity, specificity

def f1_plot(input_img, annotations, out_img, spacing=40):
    label_img = measure.label(np.array(input_img))

    #Finding max mass, area for thresholding
    mass = area = 0
    for region in measure.regionprops(label_img, input_img):
        mass = max(mass, region.weighted_moments[0][0])
        area = max(area, region.area)

    area_stats = []
    mass_stats = []

#     print('Area Thresholding')
    for area_threshold in np.linspace(0, 40, num=spacing):
#         print(area_threshold)
        region_thresh = []
        for region in measure.regionprops(label_img, input_img):
            if region.area >= area_threshold:
                region_thresh.append(region)

        overlap_dict = overlap(region_thresh, annotations)
        area_stats.append(compute_stats(overlap_dict))

    area_stats = np.array(area_stats)

#     print('Mass Thresholding')
    for mass_threshold in np.linspace(0, mass/3, num=spacing):
#         print(mass_threshold)
        region_thresh = []
        for region in measure.regionprops(label_img, input_img):
            if region.weighted_moments[0][0] >= mass_threshold:
                region_thresh.append(region)

        overlap_dict = overlap(region_thresh, annotations)
        mass_stats.append(compute_stats(overlap_dict))

    mass_stats = np.array(mass_stats)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    ax1.set_title('Precision/Recall Curves with Area Thresholding')
    ax1.set_xlabel('Area Threshold')
    ax1.plot(np.linspace(0, 40, num=spacing), area_stats[:,0], label='Precision')
    ax1.plot(np.linspace(0, 40, num=spacing), area_stats[:,1], label='Recall')
    ax1.plot(np.linspace(0, 40, num=spacing), area_stats[:,2], label='F-l score')
    ax1.legend()

    ax2.set_title('Precision/Recall Curves with Mass Thresholding')
    ax2.set_xlabel('Mass Threshold')
    ax2.plot(np.linspace(0, mass, num=spacing), mass_stats[:,0], label='Precision')
    ax2.plot(np.linspace(0, mass, num=spacing), mass_stats[:,1], label='Recall')
    ax2.plot(np.linspace(0, mass, num=spacing), mass_stats[:,2], label='F-l score')
    ax2.legend()
    plt.savefig(out_img, dpi=300)


    area_max_f1 = np.argmax(area_stats[:,2])
    mass_max_f1 = np.argmax(mass_stats[:,2])

    return (area_stats[area_max_f1, 0:3], mass_stats[mass_max_f1])


def overlay_annotations_cc(input_img, annotations, title='', area_thresh=5, mass_thresh=5000):
    plt.figure(figsize=(20, 10))
    fig = plt.gcf()
    ax = plt.gca()

    ax.set_title(title)
    ax.imshow(input_img)

    label_im = measure.label(np.array(input_img))

    purple_centers_r = []
    red_centers_r = []
    blue_centers_r = []

    for region in measure.regionprops(label_im, input_img):
        if region.area >= area_thresh and region.weighted_moments[0][0] >= mass_thresh:
            # draw rectangle around segmented points
            minr, minc, maxr, maxc = region.bbox
            rect = mpl.patches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                      fill=False, edgecolor='purple', linewidth=2)
            ax.add_patch(rect)
            purple_centers_r.append(region.centroid)

        elif region.weighted_moments[0][0] >= mass_thresh:
            minr, minc, maxr, maxc = region.bbox
            rect = mpl.patches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                      fill=False, edgecolor='blue', linewidth=2)
            ax.add_patch(rect)
            blue_centers_r.append(region.centroid)


        elif region.area >= area_thresh:
            minr, minc, maxr, maxc = region.bbox
            rect = mpl.patches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                      fill=False, edgecolor='red', linewidth=2)
            ax.add_patch(rect)
            red_centers_r.append(region.centroid)

    for idx, row in annotations.iterrows():
        x = row['X'] + row['Width']/2
        y = row['Y'] + row['Height']/2
        elps = mpl.patches.Ellipse((x,y), width=row['Width'], height=row['Height'], edgecolor='g', lw=2, facecolor='none')
        ax.add_patch(elps)

    red_patch = mpl.patches.Patch(color='red', label='Predicted synapses with area >= {}'.format(area_thresh))
    blue_patch = mpl.patches.Patch(color='blue', label='Predicted synapses with mass >= {}'.format(mass_thresh))
    purple_patch = mpl.patches.Patch(color='purple', label='Predicted synapses with high mass and area')
    annotation_patch = mpl.patches.Patch(color='green', label='Annotated centroids')

    plt.legend(handles=[red_patch, blue_patch, purple_patch, annotation_patch], bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.3)
    scalebar = ScaleBar(0.09, 'um', length_fraction=0.1, height_fraction=0.005, color='k', border_pad=0.3) # 1 pixel = 0.09 um
    ax.add_artist(scalebar)
    ax.axis('off');

def stats_multithreshold(input_img, annotations, spacing=40):
    label_img = measure.label(np.array(input_img))

    #Finding max mass, area for thresholding
    mass = area = 0
    for region in measure.regionprops(label_img, input_img):
        mass = max(mass, region.weighted_moments[0][0])
        area = max(area, region.area)

    stats = []

    for area_threshold in np.linspace(0, 40, num=spacing):
        for mass_threshold in np.linspace(0, mass/3, num=spacing):
#             print('Area = {}\nMass = {}'.format(area_threshold, mass_threshold))
            region_thresh = []
            for region in measure.regionprops(label_img, input_img):
                if region.weighted_moments[0][0] >= mass_threshold \
                    and region.area >= area_threshold:
                    region_thresh.append(region)

            overlap_dict = overlap(region_thresh, annotations)
            stats.append(compute_stats(overlap_dict))

    return stats
