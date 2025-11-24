#!/usr/bin/env python3
#*******************************************************************************
#rrr_riv_tot_gen_all_sword.py
#*******************************************************************************

#Purpose:
#Given a river shapefile from SWORD, and given an expected maximum number 
#of upstream river reaches per reach, this program creates a series of csv files
#with the following information:
# - rrr_kfc_csv
#   . Travel time for flow wave at 1km/hour
# - rrr_xfc_csv
#   . The value 0.3
# - rrr_crd_csv
#   . River ID
#   . Longitude of a point related to each river reach
#   . Latitude of a point related to each river reach
#
#The benefit of generating all these files together is to ensure that they are 
#sorted in a similar manner.
#Author:
#Cedric H. David, 2022-2022


#*******************************************************************************
#Import Python modules
#*******************************************************************************
import sys
import fiona
import shapely.geometry
import csv


#*******************************************************************************
#Declaration of variables (given as command line arguments)
#*******************************************************************************
# 1 - mer_riv_shp
# 2 - rrr_kfc_csv
# 3 - rrr_xfc_csv
# 4 - rrr_crd_csv

# python rrr_riv_tot_gen_all_sword.py \
#         /Users/elyssac/Documents/RiverRouting/inputs/b82/Main_Side/na_sword_reaches_hb82_v17_rte.shp \
#         /Users/elyssac/Documents/RiverRouting/inputs/b82/Main_Side/k_82.csv \
#         /Users/elyssac/Documents/RiverRouting/inputs/b82/Main_Side/xfc_82.csv \
#         /Users/elyssac/Documents/RiverRouting/inputs/b82/Main_Side/coords_82.csv 

#*******************************************************************************
#Get command line arguments
#*******************************************************************************
IS_arg=len(sys.argv)
if IS_arg != 5:
     print('ERROR - Only 4 argument can be used')
     raise SystemExit(22) 

mer_riv_shp=sys.argv[1]
rrr_kfc_csv=sys.argv[2]
rrr_xfc_csv=sys.argv[3]
rrr_crd_csv=sys.argv[4]

# mer_riv_shp='../test/na_sword_reaches_hb82_v17_rte.shp'
# rrr_kfc_csv='../test/k_82.csv'
# rrr_xfc_csv='../test/xfc_82.csv'
# rrr_crd_csv='../test/coords_82.csv'

#*******************************************************************************
#Print input information
#*******************************************************************************
print('Command line inputs')
print('- '+mer_riv_shp)
print('- '+rrr_kfc_csv)
print('- '+rrr_xfc_csv)
print('- '+rrr_crd_csv)


#*******************************************************************************
#Check if files exist 
#*******************************************************************************
try:
     with open(mer_riv_shp) as file:
          pass
except IOError as e:
     print('ERROR - Unable to open '+mer_riv_shp)
     raise SystemExit(22) 


#*******************************************************************************
#Read shapefile
#*******************************************************************************
print('Read shapefile')

#-------------------------------------------------------------------------------
#Open file 
#-------------------------------------------------------------------------------
print('- Open file')

mer_riv_lay=fiona.open(mer_riv_shp, 'r')
IS_riv_tot=len(mer_riv_lay)
print('- The number of river features is: '+str(IS_riv_tot))

#-------------------------------------------------------------------------------
#Read attributes
#-------------------------------------------------------------------------------
print('- Read attributes')

if 'reach_id' in mer_riv_lay[0]['properties']:
     YV_riv_id='reach_id'
else:
     print('ERROR - reach_id does not exist in '+mer_riv_shp)
     raise SystemExit(22) 

if 'reach_len' in mer_riv_lay[0]['properties']:
     YV_riv_lkm='reach_len'
else:
     print('ERROR - reach_len does not exist in '+mer_riv_shp)
     raise SystemExit(22) 

IV_riv_tot_id=[]
ZV_riv_lkm=[]
for JS_riv_tot in range(IS_riv_tot):
     IV_riv_tot_id.append(int(mer_riv_lay[JS_riv_tot]['properties'][YV_riv_id]))
     ZV_riv_lkm.append(float(mer_riv_lay[JS_riv_tot]['properties'][YV_riv_lkm]) / 1000)

#-------------------------------------------------------------------------------
#Reading shapes
#-------------------------------------------------------------------------------
print('- Read shapes')

ZV_x_ups=[]
ZV_y_ups=[]
ZV_x_dwn=[]
ZV_y_dwn=[]
ZV_x_crd=[]
ZV_y_crd=[]
for JS_riv_tot in range(IS_riv_tot):
     mer_riv_crd=mer_riv_lay[JS_riv_tot]['geometry']['coordinates']
     #If it's a multilinestring, merge into one linestring
     if mer_riv_lay[JS_riv_tot]["geometry"]['type']=='MultiLineString':
          # merged_line = shapely.ops.linemerge(mer_riv_lay[JS_riv_tot]["geometry"]['coordinates'])
          mer_riv_crd_tmp = mer_riv_crd[0]
          for i in range(1,len(mer_riv_crd)):
               mer_riv_crd_tmp.extend(mer_riv_crd[i])
          mer_riv_crd = mer_riv_crd_tmp
     
     IS_point=len(mer_riv_crd)
     #Upstream and downstream points of each polyline:
     ZV_x_dwn.append(mer_riv_crd[0][0])
     ZV_y_dwn.append(mer_riv_crd[0][1])
     ZV_x_ups.append(mer_riv_crd[IS_point-1][0])
     ZV_y_ups.append(mer_riv_crd[IS_point-1][1])
     #Second to last downstream points for each polyline:
     ZV_x_crd.append(mer_riv_crd[1][0])
     ZV_y_crd.append(mer_riv_crd[1][1])


##*******************************************************************************
#Compute pfac
#*******************************************************************************
print('Processing routing parameters')
ZV_kfac=[float(0)] * IS_riv_tot
ZV_xfac=[float(0)] * IS_riv_tot

for JS_riv_tot in range(IS_riv_tot):
     ZV_kfac[JS_riv_tot]=ZV_riv_lkm[JS_riv_tot]*1000*3.6
     ZV_kfac[JS_riv_tot]=ZV_kfac[JS_riv_tot]*0.35 #Multiplying by medium lambdak in Collins et al., 2024
     ZV_xfac[JS_riv_tot]=0.3

#*******************************************************************************
#Write outputs
#*******************************************************************************
print('Writing files')


with open(rrr_kfc_csv, 'w') as csvfile:
     csvwriter = csv.writer(csvfile, dialect='excel')
     for JS_riv_tot in range(IS_riv_tot):
          csvwriter.writerow([round(ZV_kfac[JS_riv_tot],4)])

with open(rrr_xfc_csv, 'w') as csvfile:
     csvwriter = csv.writer(csvfile, dialect='excel')
     for JS_riv_tot in range(IS_riv_tot):
          csvwriter.writerow([ZV_xfac[JS_riv_tot]]) 

with open(rrr_crd_csv, 'w') as csvfile:
     csvwriter = csv.writer(csvfile, dialect='excel')
     for JS_riv_tot in range(IS_riv_tot):
          IV_line=[IV_riv_tot_id[JS_riv_tot], 
                   ZV_x_crd[JS_riv_tot], 
                   ZV_y_crd[JS_riv_tot]] 
          csvwriter.writerow(IV_line) 


#*******************************************************************************
#End
#*******************************************************************************
