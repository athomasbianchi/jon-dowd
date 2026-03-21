import pandas as pd

# player universe
TJ_ID = "tj_id"
FG_ID = "fg_id"
ESPN_ID = "espn_id"
NAME = "name"
NAME_ASCII = "name_ascii"
MLB_ID = "mlb_id"

# contracts
CONTRACT_ID = "contract_id"
CONTRACT_TYPE = "contract_type"
CONTRACT_YEARS = "contract_years"
CONTRACT_DOLLARS = "contract_dollars"
AA_OPTIONS = "aa_options"
AAA_OPTIONS = "aaa_options"
ARB_RATE = "arb_rate"
# remove dup, nameascii, original team, fgid
# ref tj_id, team_id

# draft
PICK_ID = "pick_id"
PICK_YEAR = "pick_year"
PICK_ROUND = "pick_round"
PICK_ORDER = "pick_order"
PICKING_TEAM_ID = "pick_team_id"
ORIGINAL_TEAM_ID = "pick_original_team_id"
TRADED_TEAM_ID = "pick_traded_team_id"
# remove picking_team_abbr, original_team_abbr, traded_team_abbr

# teams
TEAM_ID = "team_id"
TEAM_NAME = "team_name"
TEAM_LEVEL = "team_;evel"
TEAM_ABBR = "team_abbr"

# player_info
PLAYER_MLB_ORG = "player_mlb_org"
PLAYER_POS = "player_pos"
PLAYER_AGE = "player_age"
PLAYER_JERSEY = "player_jersey"

# player elig
C = "c"
FIRST = "1b"
SECOND = "2b"
SS = "ss"
THIRD = "3b"
OF = "of"
UTIL = "util"
SP = "sp"
RP = "rp"

e_df = pd.read_csv('../data/input_download/espn_proj.csv')
id_df = pd.read_csv('../data/output_final/tj_id_map.csv')
con_df = pd.read_csv('../data/output_final/contracts.csv')
teams_df = pd.read_csv('../data/output_final/teams.csv')
proj_df = pd.read_csv('../data/output_final/projections.csv')
elig_df = pd.read_csv('../data/output_final/elig.csv')
info_df = pd.read_csv('../data/output_final/player_info.csv')

id_df[ESPN_ID] = id_df[ESPN_ID].astype("Int64")


# print(e_df.head())
# print(elig_df.head())
# print(id_df.head())
# print(con_df.head())

# aaa options list TODO add positions
# aaa_opts_df = con_df[con_df['aaa_options'] == True]
# aaa_opts_df = pd.merge(left=aaa_opts_df, right=id_df, on=TJ_ID, indicator=True, how='left')
# aaa_opts_df = aaa_opts_df[['Original Team', 'team_id', 'NameASCII_x', 'tjid', 'fgId_x', 'espnId', 'type', 'years', 'dollars', 'aaa_options']]
# # aaa_opts_df['espnId'] = aaa_opts_df['espnId'].astype('Int64')
# aaa_opts_df.rename(columns={'fg_id_x': 'fgId', 'NameASCII_x': 'NameASCII'}, inplace=True)
# aaa_opts_df = pd.merge(left=aaa_opts_df, right=proj_df, how='left', on='fgId')
# aaa_opts_df.sort_values(by='fp_avg', ascending=False, inplace=True)
# aaa_opts_df.rename(columns={'NameASCII_x': 'NameASCII', 'tjid_x': 'tjid' }, inplace=True)
# aaa_opts_df = aaa_opts_df[['Original Team', 'team_id', 'NameASCII', 'tjid', 'type', 'years', 'dollars', 'fp_avg']]
# aaa_opts_df = aaa_opts_df[['Original Team', 'NameASCII',]]
# aaa_opts_df.to_csv("../share/aaa.csv", index=False)

# arb list TODO add positions
# arb_df = con_df[con_df['arb_rate'] > 0]

# arb_df = pd.merge(arb_df, id_df, on=TJ_ID, how='left')
# arb_df = pd.merge(arb_df, e_df, how='left', left_on=ESPN_ID, right_on='id')
# arb_df.sort_values(['arb_rate', 'total_25'], ascending=[False, False], inplace=True)
# print(arb_df.columns)
# arb_df = arb_df[['team_id', NAME_ASCII, TJ_ID, 'type', 'arb_rate', 'total_25']]
# arb_df = arb_df[['Original Team', 'NameASCII_x', 'type', 'arb_rate', 'total_25']]
# arb_df.rename(columns={'NameASCII_x': 'player'}, inplace=True)
# arb_df.to_csv("../share/arb.csv", index=False)

# FA LIST
e_id_df = pd.merge(left=id_df, right=elig_df, on=TJ_ID, how="left")
fa_df = pd.merge(left=e_df, right=e_id_df, left_on='id', right_on=ESPN_ID, how='left')
fa_df = pd.merge(left=fa_df, right=con_df, on=TJ_ID, how='left')
fa_df = pd.merge(left=fa_df, right=teams_df, on='team_id', how='left')
fa_df = pd.merge(left=fa_df, right=info_df, on=TJ_ID, how='left')
fa_df = pd.merge(left=fa_df, right=proj_df, on=TJ_ID, how='left')
print(fa_df.columns)
fa_df = fa_df[
    [
        "name_x",
        "player_mlb_org",
        "player_age",
        C,
        FIRST,
        SECOND,
        THIRD,
        SS,
        OF,
        UTIL,
        SP,
        RP,
        "contract_type",
        "abbrev",
        "contract_years",
        "contract_dollars",
        "fp_atc",
        "fp_alt",
        "alt-atc",
        "fp_avg",
        "fp_e",
        "atc-e",
    ]
]
fa_df.rename(columns={'name_x': 'name'}, inplace=True)
# fa_df.fillna("", inplace=True)

def pos_string(row):
  pos_string = ""
  if row[SECOND] == True:
    if len(pos_string) > 0:
      pos_string += "/"
    pos_string += "2B"
  if row[THIRD] == True:
    if len(pos_string) > 0:
      pos_string += "/"
    pos_string += "3B"
  if row[C] == True:
    if len(pos_string) > 0:
      pos_string += "/"
    pos_string += "C"
  if row[FIRST] == True:
    if len(pos_string) > 0:
      pos_string += "/"
    pos_string += "1B"
  if row[SS] == True:
    if len(pos_string) > 0:
      pos_string += "/"
    pos_string += "SS"
  if row[OF] == True:
    if len(pos_string) > 0:
      pos_string += "/"
    pos_string += "OF"
  if row[UTIL] == True: 
    if len(pos_string) > 0:
      pos_string += "/"
    pos_string += "UTIL"
  if row[SP] == True:
    if len(pos_string) > 0:
      pos_string += "/"
    pos_string += "SP"
  if row[RP] == True:
    if len(pos_string) > 0:
      pos_string += "/"
    pos_string += "RP"
  return pos_string

fa_df['pos_string'] = fa_df.apply(pos_string, axis=1)


c_df = fa_df[fa_df[C] == True].reset_index(drop=True)
first_df = fa_df[fa_df[FIRST] == True].reset_index(drop=True)
second_df = fa_df[fa_df[SECOND] == True].reset_index(drop=True)
third_df = fa_df[fa_df[THIRD] == True].reset_index(drop=True)
ss_df = fa_df[fa_df[SS] == True].reset_index(drop=True)
of_df = fa_df[fa_df[OF] == True].reset_index(drop=True)
sp_df = fa_df[fa_df[SP] == True].reset_index(drop=True)
rp_df = fa_df[fa_df[RP] == True].reset_index(drop=True)
ut_df = fa_df[(fa_df[UTIL] == True) & (fa_df[FIRST] == False) & (fa_df[C] == False) & (fa_df[SECOND] == False) & (fa_df[THIRD] == False) & (fa_df[SS] == False) & (fa_df[OF] == False)].reset_index(drop=True)
display_list = [
    "name",
    "pos_string",
    "player_mlb_org",
    "player_age",
    "abbrev",
    "contract_type",
    "contract_years",
    "contract_dollars",
    "fp_atc",
    "fp_alt",
    "alt-atc",
    "fp_avg",
    "fp_e",
    "atc-e", 
]


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
