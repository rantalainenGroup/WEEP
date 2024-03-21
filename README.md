# WEEP: Wsi rEgion sElection aPproach

This repo includes the implementation steps of the methodology WEEP. <br />   
It includes the example of the implementation of the WEEP on the tile-level prediction scores for breast cancer histological grade 1 vs 3 classification. <br />   
The tile-to-slide aggregation function was used as the 75th percentile of the tile-level scores as used in the study but different summary statistics-based aggregation like mean, median can be easily implemented by modifying the '''weep_per_slide''' function in weep.py


