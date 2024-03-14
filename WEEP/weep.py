import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import random
import pickle
import matplotlib

def weep_batch(df:pd.DataFrame):
    '''
    applying weep to a set of wsis
    :param df: dataframe expected to include the columns:
    df['slide_name'] <- slide names ,
    df['tile_filename'] <- tile names,
    df['pred_scores'] <- tile-level prediction scores e.g., class probabilities,
    classification threshold for that slide <- df['threshold']
    :return: df with selected tiles for each WSI and the tile-level prediction score
    '''
    # list of df containing the selected tiles for each WSI
    dfs = []
    wsi_list = df.slide_name.tolist()
    for slide in tqdm(wsi_list):
        # initiating a df to store the selected tiles using weep and prediction scores
        df_selected_tiles = pd.DataFrame()
        df_tmp = df.copy()
        df_tmp_slide = df_tmp.loc[df_tmp['slide_name'] == slide]

        # get the threshold value for that slide
        threshold = df_tmp_slide.iloc[0]['threshold']
        # applying weep for that slide
        tile_names, pred_scores = weep_per_slide(df_tmp_slide, threshold)
        df_selected_tiles['tile_filename'] = tile_names
        df_selected_tiles['pred_scores'] = pred_scores
        df_selected_tiles['slide_name'] = slide
        dfs.append(df_selected_tiles)

    # concatenating the dfs containing the selected tiles for each wsi
    df_selected = pd.concat(dfs)
    df_selected = df_selected.reset_index(drop=True)

    return df_selected




def weep_per_slide(df: pd.DataFrame, threshold):
    '''
    Applying weep to a slide
    :param df: data frame including the columns tile-level prediction scores,
    and tile file names i.e. df['tile_filename']
    :param threshold: classification threshold for the binary classification
    :return: list of selected tiles through weep and the list of prediction scores
    '''

    # df_tmp = df.copy()
    # sorting the prediction scores in the descending order
    df = df.sort_values(by='pred_scores', ascending=False)
    tile_names = []
    pred_scores = []

    # iterate through the ranked prediction scores
    for i in tqdm(range(len(df))):
        # calculating the slide-level prediction score after dropping the highest ranked tile
        df_tmp = df.drop([i])
        # here we use the 75th percentile of the pred scores as the aggregation function
        slide_score = df_tmp['pred_scores'].quantile(0.75)
        if slide_score >= threshold:
            # storing the tile names and slide scores
            tile_names.append(df.iloc[i]['tile_filename'])
            pred_scores.append(slide_score)


        else:
            break

    return tile_names, pred_scores




