###################################################
# Script: generate_widths.py
# Usage: Getting prior river widths from SWORD for routing
#           - IDs are sorted the same as riv/bas file
###################################################

import os
import numpy as np
import pandas as pd
import geopandas as gpd


#*******************************************************************************
#Inputs
#*******************************************************************************

#### Basin 82
riv_shp = '../test/na_sword_reaches_hb82_v17.shp'
srt_csv = '../test/riv_82.csv'
wid_csv = '../test/widths_82.csv'


#*******************************************************************************
#Processing
#*******************************************************************************
riv = pd.read_csv(srt_csv, header=None)

## Calculated sinuosity in QGIS: https://gis.stackexchange.com/questions/256622/adding-line-sinuosity-with-pyqgis
## reach_len / distance(start_point($geometry), end_point( $geometry))
## Sinuosity stored as column in SWORD riv_shp

sword = gpd.read_file(riv_shp)

## Width-only
sword_sub = sword[['reach_id', 'width']]

## Width and reach length
# sword_sub = sword[['reach_id', 'width', 'reach_len']]
# sword_sub['wid_len'] = sword_sub['width'] * sword_sub['reach_len']
# sword_sub = sword_sub[['reach_id', 'wid_len']]

## Width and sinuosity
# sword_sub = sword[['reach_id', 'width', 'sinuosity']]
# sword_sub['wid_sin'] = sword_sub['width'] * sword_sub['sinuosity']
# sword_sub = sword_sub[['reach_id', 'wid_sin']]


key = pd.Series({k:v for v,k in enumerate(riv.iloc[:,0].unique())})

sword_sub_srt = sword_sub.sort_values(by='reach_id', key=key.reindex, na_position='last')


sword_sub_srt.iloc[:,1].to_csv(wid_csv, header=None, index=None)