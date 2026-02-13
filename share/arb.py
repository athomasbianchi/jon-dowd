import pandas as pd

e_df = pd.read_csv('../input_download/espn_proj.csv')
id_df = pd.read_csv('../output/tj_id_map.csv')
con_df = pd.read_csv('../output/contracts.csv')
teams_df = pd.read_csv('../output/teams.csv')
proj_df = pd.read_csv('../output/projections.csv')
elig_df = pd.read_csv('../output/elig.csv')

id_df["espnId"] = id_df["espnId"].astype("Int64")


# print(e_df.head())
# print(elig_df.head())
# print(id_df.head())
# print(con_df.head())

# aaa options list TODO add positions
aaa_opts_df = con_df[con_df['aaa_options'] == True]
aaa_opts_df = pd.merge(left=aaa_opts_df, right=id_df, on='tjid', indicator=True, how='left')
aaa_opts_df = aaa_opts_df[['Original Team', 'team_id', 'NameASCII_x', 'tjid', 'fgId_x', 'espnId', 'type', 'years', 'dollars', 'aaa_options']]
# aaa_opts_df['espnId'] = aaa_opts_df['espnId'].astype('Int64')
aaa_opts_df.rename(columns={'fgId_x': 'fgId', 'NameASCII_x': 'NameASCII'}, inplace=True)
aaa_opts_df = pd.merge(left=aaa_opts_df, right=proj_df, how='left', on='fgId')
aaa_opts_df.sort_values(by='fp_avg', ascending=False, inplace=True)
aaa_opts_df.rename(columns={'NameASCII_x': 'NameASCII', 'tjid_x': 'tjid' }, inplace=True)
aaa_opts_df = aaa_opts_df[['Original Team', 'team_id', 'NameASCII', 'tjid', 'type', 'years', 'dollars', 'fp_avg']]
aaa_opts_df = aaa_opts_df[['Original Team', 'NameASCII',]]
aaa_opts_df.to_csv("../share/aaa.csv", index=False)

# arb list TODO add positions
arb_df = con_df[con_df['arb_rate'] > 0]

arb_df = pd.merge(arb_df, id_df, on='tjid', how='left')
arb_df = pd.merge(arb_df, e_df, how='left', left_on='espnId', right_on='id')
arb_df.sort_values(['arb_rate', 'total_25'], ascending=[False, False], inplace=True)
arb_df = arb_df[['Original Team', 'team_id', 'NameASCII_x', 'tjid', 'type', 'arb_rate', 'total_25']]
arb_df = arb_df[['Original Team', 'NameASCII_x', 'type', 'arb_rate', 'total_25']]
arb_df.rename(columns={'NameASCII_x': 'player'}, inplace=True)
arb_df.to_csv("../share/arb.csv", index=False)

# FA LIST
fa_df = pd.merge(left=e_df, right=elig_df, left_on='id', right_on='espnId', how='left')
fa_df = pd.merge(left=fa_df, right=con_df, on='tjid', how='left')
fa_df = pd.merge(left=fa_df, right=teams_df, on='team_id', how='left')
fa_df = fa_df[['name_x', 'proj', 'C', '1B', '2B', '3B', 'SS', 'OF', 'Util', 'SP', 'RP', 'type', 'abbrev']]
fa_df.rename(columns={'name_x': 'name'}, inplace=True)
fa_df.fillna("", inplace=True)

c_df = fa_df[fa_df['C'] == True].reset_index(drop=True)
first_df = fa_df[fa_df['1B'] == True].reset_index(drop=True)
second_df = fa_df[fa_df['2B'] == True].reset_index(drop=True)
third_df = fa_df[fa_df['3B'] == True].reset_index(drop=True)
ss_df = fa_df[fa_df['SS'] == True].reset_index(drop=True)
of_df = fa_df[fa_df['OF'] == True].reset_index(drop=True)
sp_df = fa_df[fa_df['SP'] == True].reset_index(drop=True)
rp_df = fa_df[fa_df['RP'] == True].reset_index(drop=True)
ut_df = fa_df[(fa_df['Util'] == True) & (fa_df['1B'] == False) & (fa_df['C'] == False) & (fa_df['2B'] == False) & (fa_df['3B'] == False) & (fa_df['SS'] == False) & (fa_df['OF'] == False)].reset_index(drop=True)
display_list = ['name', 'proj', 'abbrev', 'type']


sp_df = sp_df[display_list]
rp_df = rp_df[display_list]
c_df = c_df[display_list]
first_df = first_df[display_list]
second_df = second_df[display_list]
third_df = third_df[display_list]
of_df = of_df[display_list]
ss_df = ss_df[display_list]
ut_df = ut_df[display_list]

sp_df.to_csv("../share/fa_sp.csv", index=False)
rp_df.to_csv("../share/fa_rp.csv", index=False)
ut_df.to_csv("../share/fa_ut.csv", index=False)
c_df.to_csv("../share/fa_c.csv", index=False)
first_df.to_csv("../share/fa_1b.csv", index=False)
second_df.to_csv("../share/fa_2b.csv", index=False)
third_df.to_csv("../share/fa_3b.csv", index=False)
ss_df.to_csv("../share/fa_ss.csv", index=False)
of_df.to_csv("../share/fa_of.csv", index=False)

