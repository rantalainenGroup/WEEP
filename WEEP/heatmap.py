import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import random
import pickle
import matplotlib
import openslide

def view_wsi(path_to_slide, level):
    '''
    function to a WSI at the given resolution level using openslide
    :param path_slide: string containing the path to the WSI
    :param level: integer value to define the resolution level for extracting the wsi from the macro image
    :return: WSI at the given resolution
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
    :param alpha: floating value between 0 and 1
    :return:
    '''
    cancer_mask = pickle.load(
        open(path_to_mask, "rb"))
    plt.imshow(cancer_mask, cmap=matplotlib.colors.ListedColormap(['w', 'c']), alpha=alpha)
    plt.axis('off')

def heatmap(df):
    '''
    plotting the heatmap of the tile-level prediction scores for that wsi
    :param df:
    :return:
    '''
    idx_batch = df.index
    for i in idx_batch:
