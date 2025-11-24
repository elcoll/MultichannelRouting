#!/usr/bin/env python3
# *****************************************************************************
# rrr_riv_rat.py
# *****************************************************************************

# Purpose:
# Given a river connectivity csv (rrr_con_csv), a csv containing river IDs
# sorted from upstream to downstream (rrr_bas_csv), and an optional width csv 
# sorted the same as rrr_bas_csv (rrr_wid_csv), calculate the ratio of 
# discharge that should go into each downstream reach. If there is only 1 
# downstream reach, the ratio is 1. If there is more than 1 downstream reach, 
# the ratio is proportional to the downstream river widths. If no width csv is 
# provided, the script assumes the maximum number of downstream reaches in the 
# basin is 1 and therefore sets the ratio for each downstream segment as 1. 
# The output csv (rrr_rat_csv) is sorted the same as rrr_bas_csv and contains 
# the following information:
# - rrr_rat_csv
#   . River ID
#   . [ID of 1st downstream river, ratio]
#   . [ID of 2nd downstream river, ratio]
#   . (...)
#   . [ID of nth downstream river, ratio]
# Author:
# Elyssa L. Collins and Cedric H. David, 2024-2024


# *****************************************************************************
# Import Python modules
# *****************************************************************************
import sys
import csv


# *****************************************************************************
# Declaration of variables (given as command line arguments)
# *****************************************************************************
# 1 - rrr_con_csv
# 2 - rrr_bas_csv
# 3 - rrr_rat_csv
# (4) - rrr_wid_csv


# *****************************************************************************
# Get command line arguments
# *****************************************************************************
IS_arg = len(sys.argv)
if (IS_arg != 4) & (IS_arg != 5):
    print('ERROR - a maximum of 4 and a minimum of 3 arguments can be used')
    raise SystemExit(22)

rrr_con_csv = sys.argv[1]
rrr_bas_csv = sys.argv[2]
rrr_rat_csv = sys.argv[3]
if IS_arg == 5:
    rrr_wid_csv = sys.argv[4]

# rrr_con_csv = '/Users/elyssac/Documents/RiverRouting/inputs/b82/Main_Side/con_82.csv'
# rrr_bas_csv = '/Users/elyssac/Documents/RiverRouting/inputs/b82/Main_Side/riv_82.csv'
# rrr_wid_csv = '/Users/elyssac/Documents/RiverRouting/inputs/b82/Main_Side/widths_82.csv'
# rrr_rat_csv = '/Users/elyssac/Documents/RiverRouting/inputs/b82/Main_Side/con_rat_82.csv'

# rrr_con_csv = '../test/con_82.csv'
# rrr_bas_csv = '../test/riv_82.csv'
# rrr_wid_csv = '../test/widths_82.csv'
# rrr_rat_csv = '../test/con_rat_82.csv'


# *****************************************************************************
# Print input information
# *****************************************************************************
print('Command line inputs')
print(' - ' + rrr_con_csv)
print(' - ' + rrr_bas_csv)
print(' - ' + rrr_rat_csv)
if IS_arg == 5:
    print(' - ' + rrr_wid_csv)



# *****************************************************************************
# Check if files exist
# *****************************************************************************
try:
    with open(rrr_con_csv) as file:
        pass
except IOError as e:
    print('ERROR - Unable to open {0.filename}'.format(e))
    raise SystemExit(22)

try:
    with open(rrr_bas_csv) as file:
        pass
except IOError as e:
    print('ERROR - Unable to open {0.filename}'.format(e))
    raise SystemExit(22)

if IS_arg == 5:
    try:
        with open(rrr_wid_csv) as file:
            pass
    except IOError as e:
        print('ERROR - Unable to open {0.filename}'.format(e))
        raise SystemExit(22)


# *****************************************************************************
# Read inputs
# *****************************************************************************
print('Read inputs')

# -----------------------------------------------------------------------------
# Read connectivity file
# -----------------------------------------------------------------------------
print('- Read connectivity file')

IV_riv_tot_id = []
IV_riv_tot_dn = []
ZV_num_dwn = []
with open(rrr_con_csv) as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        ZV_num_dwn.append(int(row[1]))
        IV_riv_row_dn = []
        for JS_dwn in range(int(row[1])):
            IV_riv_row_dn.append(int(row[JS_dwn + 2]))
        IV_riv_tot_id.append(int(row[0]))
        IV_riv_tot_dn.append(IV_riv_row_dn)
IS_riv_tot = len(IV_riv_tot_id)

print('  . The number of river reaches in connectivity file is: '
      + str(IS_riv_tot))

print('  . The maximum number of downstream river reaches is: '
      + str(max(ZV_num_dwn)))

# -----------------------------------------------------------------------------
# Read basin file
# -----------------------------------------------------------------------------
print('Reading basin file')

IV_riv_bas_id = []
with open(rrr_bas_csv, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        IV_riv_bas_id.append(int(row[0]))

IS_riv_bas = len(IV_riv_bas_id)
print('- Number of river reaches in rrr_bas_csv: ' + str(IS_riv_bas))

if IS_riv_bas != IS_riv_tot:
    print('ERROR - Different number of reaches in basin and network')
    raise SystemExit(22)

# -----------------------------------------------------------------------------
# Read widths file
# -----------------------------------------------------------------------------
if IS_arg == 5:
    print('- Reading widths file')
    IV_riv_wid = []
    with open(rrr_wid_csv, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            IV_riv_wid.append(float(row[0]))

    IS_riv_wid = len(IV_riv_wid)
    print('- Number of river reaches in rrr_wid_csv: ' + str(IS_riv_wid))

    if IS_riv_wid != IS_riv_tot:
        print('ERROR - Different number of reaches in widths file and network')
        raise SystemExit(22)


# *****************************************************************************
# Creating hash tables
# *****************************************************************************
print('Creating hash tables')

IM_hsh_tot = {}
for JS_riv_tot in range(IS_riv_tot):
    IM_hsh_tot[IV_riv_tot_id[JS_riv_tot]] = JS_riv_tot

IM_hsh_bas = {}
for JS_riv_bas in range(IS_riv_bas):
    IM_hsh_bas[IV_riv_bas_id[JS_riv_bas]] = JS_riv_bas

IV_riv_ix1 = [IM_hsh_bas[IS_riv_id] for IS_riv_id in IV_riv_tot_id]
IV_riv_ix2 = [IM_hsh_tot[IS_riv_id] for IS_riv_id in IV_riv_bas_id]
# These arrays allow for index mapping such that IV_riv_tot_id[JS_riv_tot]
#                                              =IV_riv_bas_id[JS_riv_bas]
# IV_riv_ix1[JS_riv_tot]=JS_riv_bas
# IV_riv_ix2[JS_riv_bas]=JS_riv_tot

print('- Hash tables created')


# *****************************************************************************
# Calculating downstream river ratios
# *****************************************************************************
print('Calculating downstream river ratios')

# Contains [reach id, downstream reach id, ratio]
ZV_wid_bas_rat = []
if IS_arg != 5:
    for JS_riv_bas in range(IS_riv_bas):
        JS_riv_tot = IM_hsh_tot[IV_riv_bas_id[JS_riv_bas]]
        if IV_riv_tot_dn[JS_riv_tot][0] == 0:
            ZV_wid_bas_rat.append([IV_riv_bas_id[JS_riv_bas],
                                   IV_riv_tot_dn[JS_riv_tot][0], 0])    
        else:
            ZV_wid_bas_rat.append([IV_riv_bas_id[JS_riv_bas],
                                   IV_riv_tot_dn[JS_riv_tot][0], 1])
else:
    print('- Widths used to calculate downstream river ratios')
    for JS_riv_bas in range(IS_riv_bas):
        JS_riv_tot = IM_hsh_tot[IV_riv_bas_id[JS_riv_bas]]
        if len(IV_riv_tot_dn[JS_riv_tot]) > 1:
            ZV_wid = []
            for JS_dwn in range(len(IV_riv_tot_dn[JS_riv_tot])):
                JS_riv_ba2 = IM_hsh_bas[IV_riv_tot_dn[JS_riv_tot][JS_dwn]]
                ZV_wid.append(IV_riv_wid[JS_riv_ba2])
            ZV_wid_rat_dn = [ZS_wid / sum(ZV_wid) for ZS_wid in ZV_wid]

            for JS_dwn in range(len(IV_riv_tot_dn[JS_riv_tot])):
                ZV_wid_bas_rat.append([IV_riv_bas_id[JS_riv_bas],
                                       IV_riv_tot_dn[JS_riv_tot][JS_dwn],
                                       round(ZV_wid_rat_dn[JS_dwn], 4)])

        elif len(IV_riv_tot_dn[JS_riv_tot]) == 1:
            # ZV_wid_bas_rat[IV_riv_tot_dn[JS_riv_tot][0]] = 1
            if IV_riv_tot_dn[JS_riv_tot][0] == 0:
                ZV_wid_bas_rat.append([IV_riv_bas_id[JS_riv_bas],
                                       IV_riv_tot_dn[JS_riv_tot][0], 0])    
            else:
                ZV_wid_bas_rat.append([IV_riv_bas_id[JS_riv_bas],
                                       IV_riv_tot_dn[JS_riv_tot][0], 1])


# ZV_wid_bas_rat[62270000211]
# ZV_wid_bas_rat.index([62270000211])
# tst = [item[1] for item in ZV_wid_bas_rat]
# [i for i in range(len(tst)) if tst[i] == 62270000211]
# [i for i in range(len(tst)) if tst[i] == 62100100386]

# tst_val = [item[2] for item in ZV_wid_bas_rat]
# tst_val[17487]
# tst_val[20954]

# ZV_wid_bas_rat[17487]
# ZV_wid_bas_rat[20954]


# *****************************************************************************
# Writing rrr_rat_csv
# *****************************************************************************
print('Writing rrr_rat_csv')

IV_wid_bas_rat_id = [IV_id[0] for IV_id in ZV_wid_bas_rat]
with open(rrr_rat_csv, 'w') as csvfile:
    csvwriter = csv.writer(csvfile, dialect='excel')
    for JS_riv_bas in range(IS_riv_bas):
        IV_ind = [IS_ind for IS_ind in range(len(IV_wid_bas_rat_id)) if
                  IV_wid_bas_rat_id[IS_ind] == IV_riv_bas_id[JS_riv_bas]]
        IV_line = [IV_riv_bas_id[JS_riv_bas]]
        for JS_dwn in range(len(IV_ind)):
            IV_line.append([ZV_wid_bas_rat[IV_ind[JS_dwn]][1],
                            ZV_wid_bas_rat[IV_ind[JS_dwn]][2]])
        IV_line = IV_line + [[0, 0]] * ((max(ZV_num_dwn) + 1) - len(IV_line))
        csvwriter.writerow(IV_line)

print('Finished')
