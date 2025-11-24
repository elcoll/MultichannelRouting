###################################################
# Script: generate_connectivity.py
# Usage: Creating connecvitity and sort files

# Generates:
# - rrr_con_csv 
#   . River ID
#   . ID of unique downstream river
#   . Number of upstream rivers
#   . ID of 1st upstream river
#   . (...)
#   . ID of nth upstream river
# - rrr_srt_csv
#   . Integer to use for sorting rivers, here a topological sort 
###################################################

import os
import geopandas as gpd
import pandas as pd
import numpy as np

#*******************************************************************************
#Inputs
#*******************************************************************************

#### Basin 82
riv_shp = '../test/na_sword_reaches_hb82_v17.shp'
con_csv = '../test/con_82.csv'
srt_csv = '../test/riv_82.csv'

#*******************************************************************************
# Processing
#*******************************************************************************

#-------------------------------------------------------
#con file
#-------------------------------------------------------


SWORD_reaches = gpd.read_file(riv_shp)

SWORD_reaches.columns
SWORD_reaches_sub = SWORD_reaches[['reach_id', 'n_rch_up', 'n_rch_dn', 'rch_id_up', 'rch_id_dn']]


con = pd.DataFrame({'reach_id': SWORD_reaches_sub.reach_id,
                    'n_rch_dn': 0,
                    'rch_id_dn_1': 0,
                    'rch_id_dn_2': 0,
                    'rch_id_dn_3': 0,
                    'rch_id_dn_4': 0,
                    'n_rch_up': 0,
                    'rch_id_up_1': 0,
                    'rch_id_up_2': 0,
                    'rch_id_up_3': 0,
                    'rch_id_up_4': 0})

# ix = 0
for ix, r in SWORD_reaches_sub.iterrows():

    ## Reach(es) downstream of current reach
    con.n_rch_dn[ix] = SWORD_reaches_sub.n_rch_dn[ix]
    if SWORD_reaches_sub.n_rch_dn[ix] == 0:
        continue
    dn_rchs = SWORD_reaches_sub.rch_id_dn[ix].split(' ')
    for n in range(SWORD_reaches_sub.n_rch_dn[ix]):
        con['rch_id_dn_' + str(n + 1)][ix] = int(dn_rchs[n])

    ## Reach(es) upstream of current reach
    con.n_rch_up[ix] = SWORD_reaches_sub.n_rch_up[ix]
    if SWORD_reaches_sub.n_rch_up[ix] == 0:
        continue
    up_rchs = SWORD_reaches_sub.rch_id_up[ix].split(' ')
    for n in range(SWORD_reaches_sub.n_rch_up[ix]):
        con['rch_id_up_' + str(n + 1)][ix] = int(up_rchs[n])


con = con.reset_index(drop=True)
con.to_csv(con_csv, header=False, index=False)




#-------------------------------------------------------
#riv file
#-------------------------------------------------------

df = pd.read_csv(con_csv, header=None)


df.columns = ['reach_id', 'n_rch_dn', 'rch_id_dn_1', 'rch_id_dn_2', 'rch_id_dn_3', 'rch_id_dn_4', 'n_rch_up', 'rch_id_up_1', 'rch_id_up_2', 'rch_id_up_3', 'rch_id_up_4']

df_sub = df[['reach_id', 'n_rch_dn', 'rch_id_dn_1', 'rch_id_dn_2', 'rch_id_dn_3']]
df_sub['reach_id'] = df_sub.reach_id.astype('str')
df_sub['rch_id_dn_1'] = df_sub.rch_id_dn_1.astype('str')
df_sub['rch_id_dn_2'] = df_sub.rch_id_dn_2.astype('str')
df_sub['rch_id_dn_3'] = df_sub.rch_id_dn_3.astype('str')
ind_no_dn = df_sub.loc[df_sub['rch_id_dn_1'] == '0'].index.to_list()
df_sub.loc[df_sub['rch_id_dn_1'] == '0', 'rch_id_dn_1'] = ''
df_sub.loc[df_sub['rch_id_dn_2'] == '0', 'rch_id_dn_2'] = ''
df_sub.loc[df_sub['rch_id_dn_3'] == '0', 'rch_id_dn_3'] = ''

# df_sub.loc[df_sub['rch_id_dn_1'] == '']
# df.loc[df['reach_id'] == 82100900135]
len(list(set(df.reach_id.to_list())))


rch_id_lst = []
rch_id_dn_lst = []
for i in range(len(df_sub)):
    rch_id_lst.append(df_sub.at[i, 'reach_id'])
    rch_id_dn_lst.append([df_sub.at[i, 'rch_id_dn_1']])

    if df_sub.at[i, 'n_rch_dn'] == 2:
        rch_id_lst.append(df_sub.at[i, 'reach_id'])
        rch_id_dn_lst.append([df_sub.at[i, 'rch_id_dn_2']])

    if df_sub.at[i, 'n_rch_dn'] == 3:
        rch_id_lst.append(df_sub.at[i, 'reach_id'])
        rch_id_dn_lst.append([df_sub.at[i, 'rch_id_dn_2']])
        rch_id_lst.append(df_sub.at[i, 'reach_id'])
        rch_id_dn_lst.append([df_sub.at[i, 'rch_id_dn_3']])
     

ind_no_dn = [i for i in range(len(rch_id_dn_lst)) if rch_id_dn_lst[i] == ['']]

for i in ind_no_dn:
    rch_id_dn_lst[i] = []


### Modifying the graph to include more than value (reach downstream) for an individual key (reach upstream)
graph_dict = dict()
for i in range(len(rch_id_lst)):
    if rch_id_lst[i] in graph_dict:
        # append the new number to the existing array at this slot
        graph_dict[rch_id_lst[i]].extend(rch_id_dn_lst[i])
    else:
        # create a new array in this slot
        graph_dict[rch_id_lst[i]] = rch_id_dn_lst[i]


def recursive_topological_sort(graph, node):
    result = []
    seen = set()

    def recursive_helper(node):
        for neighbor in graph[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                recursive_helper(neighbor)
        result.insert(0, node)              # this line replaces the result.append line

    while node:
        v = node.pop()
        if v not in seen:
            seen.add(v) # no need to append to path any more
            recursive_helper(v)

    return result


# start = list(graph)
start = list(graph_dict)
seen = set()
stack = []    # path variable is gone, stack and order are new
order = []    # order will be in reverse order at first
# q = [start]
q = start

# sort = recursive_topological_sort(graph, q)
sort = recursive_topological_sort(graph_dict, q)
sort = pd.DataFrame({'reach_id': sort})

sort.to_csv(srt_csv, header=False, index=False)

