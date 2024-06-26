import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import random
import pickle
import matplotlib


def weep_batch(df: pd.DataFrame, threshold):
    '''
    applying weep to a set of wsis
    :param df: dataframe expected to include the columns:
    df['slide_name'] <- string: slide names ,
    df['tile_filename'] <- string of tile names,
    df['pred_scores'] <- float: tile-level prediction scores e.g., class probabilities,
    :param threshold: float value: the decision threshold for the binary classification
    :return: df with selected tiles for each WSI and the tile-level prediction score
    '''
    #     if not (isinstance(df.dtypes['slide_name'], str) and isinstance(df.dtypes['tile_filename'], str)):
    #         raise TypeError('slide and tile names should be strings')

    if not isinstance(threshold, float):
        raise TypeError('threshold should be a float value between 0 and 1')

    # if not isinstance(df.dtypes['pred_scores'], float):
    #     raise TypeError('pred_scores should be float values')

    # list of df containing the selected tiles for each WSI
    dfs = []
    wsi_list = df.slide_name.unique().tolist()
    for slide in tqdm(wsi_list):
        # initiating a df to store the selected tiles using weep and prediction scores
        df_selected_tiles = pd.DataFrame()
        df_tmp = df.copy()
        df_tmp_slide = df_tmp.loc[df_tmp['slide_name'] == slide].reset_index(drop=True)
        # df_tmp_slide = df_tmp_slide
        # print(len(df_tmp_slide))

        # get the threshold value for that slide
        # threshold = df_tmp_slide.iloc[0]['threshold']
        # applying weep for that slide
        tile_names, pred_scores = weep_per_slide(df_tmp_slide, threshold)
        # print(len(tile_names), len(pred_scores))
        df_selected_tiles['tile_filename'] = tile_names
        df_selected_tiles['pred_scores'] = pred_scores
        df_selected_tiles['slide_name'] = slide
        # df_selected_tiles['threshold'] = threshold
        dfs.append(df_selected_tiles)

    # concatenating the dfs containing the selected tiles for each wsi
    df_selected = pd.concat(dfs)
    df_selected = df_selected.reset_index(drop=True)

    return df_selected


def weep_per_slide(df: pd.DataFrame, threshold):
    '''
    Applying weep to a slide
    :param df: data frame mainly including the columns tile-level prediction scores,
    and tile file names i.e. df['tile_filename']
    :param threshold: classification threshold for the binary classification
    :return: list of selected tiles through weep and the list of prediction scores
    '''


    # sorting the prediction scores in the descending order
    df = df.sort_values(by='pred_scores', ascending=False)
    df = df.reset_index(drop=True)
    df_tmp = df.copy()
    tile_names = []
    pred_scores = []

    # iterate through the ranked prediction scores
    for i in range(len(df)):
        # calculating the slide-level prediction score after dropping the highest ranked tile
        df_tmp = df_tmp.drop([i])
        # here we use the 75th percentile of the pred scores as the aggregation function
        slide_score = df_tmp['pred_scores'].quantile(0.75)

        if slide_score >= threshold:
            # storing the tile names and slide scores
            tile_names.append(df.iloc[i]['tile_filename'])
            pred_scores.append(slide_score)

        else:
            break

    return tile_names, pred_scores


def weep_plot(df:pd.DataFrame, threshold):
    '''

    :param df: df['slide_name'] <- string: slide names ,
    df['tile_filename'] <- string: tile names,
    df['pred_scores'] <- tile-level prediction scores e.g., class probabilities,
    df['threshold'] <- float: classification threshold (same for all the slides)
    :return: weep plot i.e. line plot with number of lines = number of wsis
    '''
    # retrieving the selected tiles using WEEP for the wsis in given df
    df_selected = weep_batch(df, threshold = threshold)
    wsi_list = df.slide_name.unique().tolist()
    for slide in tqdm(wsi_list):
        # storing the percentage of the selected tiles for each wsi
        percentage = []
        prediction_scores = []
        df_tmp = df_selected.loc[df_selected['slide_name'] == slide]
        df_tmp_1 = df.loc[df['slide_name'] == slide]
        # sorting the pred scores for the selected tiles for the plot
        df_tmp = df_tmp.sort_values(by='pred_scores', ascending=False)
        df_tmp = df_tmp.reset_index(drop=True)
        # print(len(df_tmp), len(df_tmp_1))
        # iterative plotting the percentage of removed tiles vs the pred scores
        for i in range(len(df_tmp)):
            percentage.append(((i+1)/len(df_tmp_1))*100)
            prediction_scores.append(df_tmp.iloc[i]['pred_scores'])
        # plotting the line plot for that wsi
        plt.plot(percentage, prediction_scores, linewidth=1)

    plt.axhline(y=threshold, label='classification threshold')
    plt.ylim(0.5, 1.0)
    # plt.xlim(0, 100)
    plt.xlabel("Removal percentage of top ranked tiles", fontsize=12)
    plt.ylabel("Slide-level prediction score", fontsize=12)
    # plt.box(False)
    # plt.spines['top'].set_visible(False)
    # plt.spines['right'].set_visible(False)
    # plt.title("Kappa vs Lower thresholds with upper_thres={}".format(upper_thres))
    plt.legend(loc="lower right", prop={'size': 8, 'weight': 'bold'})
    plt.show()

