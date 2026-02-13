import pandas as pd
import datetime
import math


PRO_TEAM_IDS = {
    0: "FA",
    1: "BAL",
    2: "BOS",
    3: "LAA",
    4: "CHW",
    5: "CLE",
    6: "DET",
    7: "KCR",
    8: "MIL",
    9: "MIN",
    10: "NYY",
    11: "ATH",
    12: "SEA",
    13: "TEX",
    14: "TOR",
    15: "ATL",
    16: "CHC",
    17: "CIN",
    18: "HOU",
    19: "LAD",
    20: "WSN",
    21: "NYM",
    22: "PHI",
    23: "PIT",
    24: "STL",
    25: "SDP",
    26: "SFG",
    27: "COL",
    28: "MIA",
    29: "ARI",
    30: "TBR",
}

DEF_POS_MAP = {
    1: "SP",
    2: "C",
    3: "1B",
    4: "2B",
    5: "3B",
    6: "SS",
    7: "OF",
    8: "OF",
    9: "OF",
    10: "DH",
    11: "RP",
}

df = pd.read_csv('../output/tj_id_map.csv')
df['MLBAMID'] = df['MLBAMID'].astype('Int64')
df['espnId'] = df['espnId'].astype('Int64')

e = pd.read_csv('../input_download/espn.csv')
e["jersey"] = e["jersey"].astype("Int64")
e["org"] = e["teamId"].apply(lambda x: PRO_TEAM_IDS[x])
e["pos"] = e["DefaultPositionId"].apply(lambda x: DEF_POS_MAP[x])

player_info = pd.merge(left=df, right=e, left_on='espnId', right_on='espnId')
player_info.sort_values(by=['rank'], inplace=True)
player_info = player_info[["tjid", 'fgId', "NameASCII", "org", "jersey", "pos"]]


player_wo_info = pd.merge(left=df, right=player_info, on='tjid', how='left', indicator=True)
player_wo_info = player_wo_info[player_wo_info['_merge'] == 'left_only']
player_wo_info = player_wo_info[['tjid', 'NameASCII_x', 'fgId_x']]
player_wo_info.rename(columns={'NameASCII_x': 'NameASCII', 'fgId_x': 'fgId'}, inplace=True)


# add prospects
fg_prospects = pd.read_csv('../input_download/2025_prospects.csv')
fg_prospects = fg_prospects[['Name', 'Org', 'Pos', 'PlayerId', 'Age']]

# calculate 2025 prospect age w/ konnor griffin info
kg_age = fg_prospects[fg_prospects['PlayerId'] == 'sa3065496']['Age']
kg_age = fg_prospects.at[0, 'Age']
kg_birthday = datetime.date(2025, 4, 24)
days_since_kg_bday = round((kg_age-19)*365,0)
date_of_rank = kg_birthday + datetime.timedelta(days=days_since_kg_bday)
days_since_71 = (date_of_rank - datetime.date(2025, 7, 1)).days
percent_of_year_passed = days_since_71 / 365

# change age to baseball age
fg_prospects['Age'] = fg_prospects['Age'].apply(lambda x: math.floor(x - percent_of_year_passed) + 1)

# add prospect info to infoless players
prospects_info = pd.merge(left=player_wo_info, right=fg_prospects, left_on='fgId', right_on='PlayerId', how='left', indicator=True)
prospects_info_success = prospects_info[prospects_info['_merge'] == 'both']
prospects_info_success = prospects_info_success[["tjid", "fgId", "NameASCII", "Org", 'Pos', 'Age']]
prospects_info_success['Age'] = prospects_info_success['Age'].astype('Int64')

# remaining players w/o info
player_wo_info = prospects_info[prospects_info['_merge'] == 'left_only']

# add mlb age by 25 results, plus 1
ages_p = pd.read_csv('../input_download/2025_ages_p.csv')
ages_h = pd.read_csv('../input_download/2025_ages_h.csv')
ages_mlb = pd.concat([ages_h, ages_p], ignore_index=True).drop_duplicates(keep='first')
ages_mlb = ages_mlb[['PlayerId', 'MLBAMID', 'NameASCII', 'Age']]
ages_mlb['Age'] = ages_mlb['Age'].apply(lambda x: x + 1)
player_info['fgId'] = player_info['fgId'].astype('string')
ages_mlb['PlayerId'] = ages_mlb['PlayerId'].astype('string')
player_info = pd.merge(left=player_info, right=ages_mlb, left_on='fgId', right_on='PlayerId')
player_info = player_info[['tjid', 'fgId', 'NameASCII_x', 'org', 'pos', 'Age', 'jersey']]
player_info.rename(columns={'NameASCII_x': 'NameASCII', 'Age': 'age'}, inplace=True)
prospects_info_success.rename(columns={'Age': 'age', 'Pos': 'pos', 'Org': 'org'}, inplace=True)
info = pd.concat([player_info, prospects_info_success], ignore_index=True, )
info = info.drop_duplicates(subset=['tjid'], keep='first')

info.to_csv('../output/player_info.csv', index=False)
player_wo_info.to_csv('./player_wo_info.csv', index=False)
