import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
from skimage import measure
import numpy as np
import seaborn as sns
import utils

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
            print('Area = {}\nMass = {}'.format(area_threshold, mass_threshold))
            region_thresh = []
            for region in measure.regionprops(label_img, input_img):
                if region.weighted_moments[0][0] >= mass_threshold \
                    and region.area >= area_threshold:
                    region_thresh.append(region)

            overlap_dict = utils.overlap(region_thresh, annotations)
            stats.append(utils.compute_stats(overlap_dict))

    return stats
