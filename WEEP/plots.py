import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import random
import pickle
import matplotlib
import openslide

def view_wsi(path_to_slide):
    '''
    function to a WSI at the given resolution level using openslide
    :param path_slide: string containing the path to the WSI
    :return: WSI at the lowest resolution
    '''
    slide = openslide.OpenSlide(path_to_slide)
    level = len(slide.level_dimensions)
    overview = slide.read_region(location=[0, 0], size=slide.level_dimensions[-1], level=level - 1)
    plt.imshow(overview)
    plt.axis('off')

def plot_cancer_mask(path_to_mask, alpha):
    '''
    plotting the cancer mask with the desired alpha
    :param path_to_mask: string containing the path to the binary mask stored as a pickle file
    :param alpha: floating value between 0 and 1 (transparency factor of the plot)
    :return: plot of the binary mask, stored as a2D array of pixels
    '''
    cancer_mask = pickle.load(
        open(path_to_mask, "rb"))
    plt.imshow(cancer_mask, cmap=matplotlib.colors.ListedColormap(['w', 'c']), alpha=alpha)
    plt.axis('off')

def heatmap(df, path_to_mask, stride, scaling_mask, pixelscaling, alpha):
    '''
    plotting the heatmap of the tile-level prediction scores for that wsi
    :param df: dataframe with tiles, tile coordinates (int), prediction score
    :param path_to_mask: string with path to the 2-D binary cancer mask stored as the pickle file
    :param stride: int value used to define the overlap between two consecutive tiles
    (no overlap = tile length in pixels for that particular resolution)
    at a particular resolution
    :param pixelscaling: float value used to scale the pixel values to tile at different resolution
    than the highest resolution (factor of 2)
    :param alpha: transparency factor for the matplotlib plot (value between 0.0 and 1.0)
    :return:
    '''
    # print(len(df))
    # path_to_mask = os.path.join(path_to_mask, '%s_AutoMask.pkl' % df_selected['slide_name'].iloc[0])
    tis_mask = pickle.load(
        open(path_to_mask, "rb"))
    h, w = tis_mask.shape
    # print(h,w)
    outputimage_probs = np.zeros(h * w).reshape(h, w)
    idx_batch = df.index
    for idx in idx_batch:
        rowi = np.floor((df.loc[idx, 'cor_x1']) / scaling_mask).astype('uint32')
        coli = np.floor((df.loc[idx, 'cor_y1']) / scaling_mask).astype('uint32')
        # print(rowi, coli)
        prediction = df.loc[idx, 'pred_scores']
        outputimage_probs[rowi:rowi + int(np.floor(stride / scaling_mask * pixelscaling)) + 1,
                          coli:coli + int(np.floor(stride / scaling_mask * pixelscaling)) + 1] = prediction
        # print(prediction, outputimage_probs)
        prob_img = outputimage_probs.copy()
    # print(prob_img)

    # plotting the binary masks
    cmap = matplotlib.colors.ListedColormap(['w', 'b'])
    bounds = [0., 0.00000000005, 1.]
    norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
    plt.imshow(prob_img, cmap=cmap, norm=norm, alpha = alpha)
    # plt.colorbar()
    plt.axis('off')
