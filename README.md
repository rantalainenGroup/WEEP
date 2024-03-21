# WEEP: Wsi rEgion sElection aPproach

This repo includes the implementation steps of the methodology WEEP as described in the paper: **WEEP: A method for spatial interpretation of weakly supervised CNN models in computational pathology**. 
It includes the example of the implementation of the WEEP on the tile-level prediction scores for breast cancer histological grade 1 vs 3 classification. The 75th percentile of the tile-level prediction scores was used as the tile-to-slide aggregation function. Different summary statistics-based aggregation like mean, median can be easily implemented by modifying the `weep_per_slide` function in `weep.py`

### Scripts and Methods

The script `weep.py` includes the functions to implement the weep over the batch of wsis using `weep_batch`. It requires the dataframe with wsis and tiles with the prediction scores along with the decision threshold for the binary classification. It implements the function `weep_per_slide` over the tiles for each WSI, applying the weep algorithm to select the tiles directly associated with the positive classification label (NHG 3 for this example) for that particular WSI. Further, the weep plot can be visualised using `weep_plot`. The `plots.py` script includes the functions to visualise the wsis (`view_wsi`), plotting the binary tumour mask (`plot_cancer_mask`), and the binary heatmap (`heatmap`) of the predicted scores for the WEEP selected regions/tiles.  

### Examples

The example of the application of WEEP have been demonstrated using three WSIs (same wsis were used in the study). The example tile dataframe (`df_tile_example.csv`) with prediction scores is included in the `examples` directory. The tumour masks and the low res WSIs examples are available in the `tumour_masks` and `wsis` sub-directories respectively. 




