# WEEP: Wsi rEgion sElection aPproach

This repo includes the implementation steps of the methodology WEEP.  It includes the example of the implementation of the WEEP on the tile-level prediction scores for breast cancer histological grade 1 vs 3 classification.    The 75th percentile of the tile-level prediction scores was used as the tile-to-slide aggregation function as it was used in the study. Different summary statistics-based aggregation like mean, median can be easily implemented by modifying the `weep_per_slide` function in `weep.py`

### Scripts and Methods

The script `weep.py` includes the functions to implement the weep over the batch of wsis using `weep_batch`. It requires the pandas df with wsis and the tiles with the prediction scores along with the decision threshold for the binary classification. It implements the function `weep_per_slide` over the tiles for each WSI, that implements the weep algorithm to select the tiles directly associated with the positive classification label (NHG 3 for this example) for the particular WSI. Further, weep plot can be visualised using `weep_plot`. The `heatmap.py` script includes the functions to visualise the wsis (`view_wsi`), plotting the binary tumour/tissue mask (`plot_cancer_mask`), and the heatmap (`heatmap`) of the predicted scores for the WEEP selected regions/tiles.  

### Examples

The example of the application of WEEP have been demonstrated using three WSIs (same wsis were used in the study). The example tile dataframe (`df_tile_example.csv`) with prediction scores is included in the `examples` directory.The tumour masks for the WSIs are available in the `tumour_masks` sub-directory.

### Software

The key software packages include `pandas v.1.5.2`, `matplotlib=3.6.2`, `numpy v.1.23.4` and `python=3.10.8`




