###################################################
# Script: generate_sorted_ratio_connectivity.py
# Usage: Ensuring that file generated from rrr_riv_rat.py 
#        (con_rat_82.csv) is sorted the same as 
#        initical connectivity (con_82.csv)
###################################################

import os
import geopandas as gpd
import pandas as pd
import numpy as np


#*******************************************************************************
#Inputs
#*******************************************************************************

#### Basin 82
con_csv = '../test/con_82.csv'
con_rat_csv = '../test/con_rat_82.csv'
con_rat_srt_csv = '../test/con_rat_82_srt.csv'

#*******************************************************************************
# Processing
#*******************************************************************************

### Sorting con_rat_82.csv to same as con_82.csv
con_82 = pd.read_csv(con_csv, header=None)
con_82_rat = pd.read_csv(con_rat_csv, header=None)

key = pd.Series({k:v for v,k in enumerate(con_82.iloc[:,0].unique())})

con_82_rat_srt = con_82_rat.sort_values(by=con_82_rat.columns[0], key=key.reindex, na_position='last')

con_82_rat_srt.to_csv(con_rat_srt_csv, header=None, index=None)
