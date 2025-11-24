# MultichannelRouting
Code for river discharge routing on river networks containing multichannels

## Input files for RiverRoutingMultichannels.py:
- con_csv (example file: 'con_rat_82_srt.csv')  
  . River ID  
  . [ID of 1st downstream river, ratio]  
  . [ID of 2nd downstream river, ratio]  
  . (...)  
  . [ID of nth downstream river, ratio]  
- m3r_ncf (example file: 'vol_82.nc')  
  . netCDF file representing inflow to the river network with dimensions (rivid,time,nv)  
  . rivid(rivid)  
  . m3_riv(rivid,time)  
  . time(time)  
  . time_bnds(time,nv)  
  . lon(lon)  
  . lat(lat)  
  . crs  
- kpr_csv (example file: 'k_82.csv')  
  . Travel time for flow wave at 1km/hour  
- xpr_csv (example file: 'xfc_82.csv')  
  . The value 0.3 for all reaches
- bas_csv (example file: 'riv_82.csv')  
  . File containing sorted river IDs (here, a topological sort)  


## More details on how to generate input files:  

**NOTE THAT MANY OF THESE SCRIPTS ARE COPIED OR ADAPTED FROM CEDRIC DAVID'S RRR REPOSITORY: https://github.com/c-h-david/rrr**  

### con_csv and bas_csv  
- Initial connectivity (without downstream ratios; i.e., 'con_82.csv') and sorted reach IDs (bas_csv, i.e., 'riv_82.csv') files created with *generate_connectivity.py*  
- Generate river widths csv (sorted the same as bas_csv) using *generate_widths.py* (wid_csv; i.e., 'widths_82.csv')  
  . Note that the reach widths csv can be replaced with (width x length), (width x sinuosity), or any other partitioning approach  
- Use initial connecitivty file, along with bas_csv and wid_csv, as inputs to *rrr_riv_rat.py*, to generate connecitivty csv of ratios for allocating water to each downstream channel (i.e., 'con_rat_82.csv')  
- Using *generate_sorted_ratio_connectivity.py*, ensure that file generated from *rrr_riv_rat.py* (con_rat_82.csv) is sorted the same as initial connectivity (con_82.csv), which produces the file: 'con_rat_82_srt.csv'

### kpr_csv  
- Generated using *rrr_riv_tot_gen_all_sword.py*  
  . Note that the attribute 'reach_len' must be in the river network shapefile and be in the units of meters  
  . Currently, this script uses a celerity = 1 km/hr and lambdak = 0.35 for all channels (main and side). Modify lambdak as needed to change the celerity.  

### xpr_csv  
- Generated using *rrr_riv_tot_gen_all_sword.py*  
  . The value for all reaches is set to 0.3  

### m3r_ncf  
- First, lat/lon coordinates are generated for each reach (i.e., 'coords_82.csv') using *rrr_riv_tot_gen_all_sword.py*  
- Calculate the contributing area for each reach and store in catch_csv (i.e., 'rapid_catchment_82.csv')  
  . catch_csv: River ID, contributing area in square kilometers, Longitude of reach / catchment centroid, Latitude of reach / catchment centroid 
- Next, generate the coupling csv (cpl_csv, i.e., 'cpl_82.csv') containing the link between the river network and the runoff netCDF grid using *rrr_cpl_riv_lsm_lnk.py*  
  . cpl_csv: River ID, Contributing catchment area in square kilometers, Longitude index (1-based) at which to look for the runoff value, Latitude index (1-based) at which to look for the runoff value  
  . Other inputs to the script include initial connectivity (i.e., 'con_82.csv'), catch_csv (i.e., 'rapid_catchment_82.csv'), and the runoff netCDF  
- Lastly, generate the runoff volume netCDF using *rrr_cpl_riv_lsm_vol.py*  
  . Inputs include initial connectivity (i.e., 'con_82.csv'), coordinates (i.e., 'coords_82.csv'), runoff netCDF, coupling file (cpl_csv, i.e., 'cpl_82.csv')  
  . Output is the runoff volume (m3r_ncf, i.e, 'vol_82.nc')  


