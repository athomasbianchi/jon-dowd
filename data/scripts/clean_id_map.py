import pandas as pd
from col_config import (
  TJ_ID,
  FG_ID,
  ESPN_ID,
  NAME,
  NAME_ASCII,
  MLB_ID
)

df = pd.read_csv('../output_to_process/tj_id_map.csv')

# rename columns
df.rename(columns={
  'fgId': FG_ID,
  'Name': NAME,
  'NameASCII': NAME_ASCII,
  'MLBAMID': MLB_ID,
  'espnId': ESPN_ID,
  'tjid': TJ_ID
}, inplace=True)

# handle types
df[MLB_ID] = df[MLB_ID].astype('Int64')
df[ESPN_ID] = df[ESPN_ID].astype('Int64')

missing_mlb_df = df[df[MLB_ID].isna() & ~df[ESPN_ID].isna()]
missing_espn_df = df[~df[MLB_ID].isna() & df[ESPN_ID].isna()]
missing_espn_df.sort_values(by='mlb_id', ascending=False, inplace=True)
print('missing mlb ids')
print(missing_mlb_df.shape)
print('missing espn ids')
print(missing_espn_df.shape)
print(missing_espn_df.head(5))

external_id_map = pd.read_csv("../input_download/id_map.csv")

mlb_merge = pd.merge(left=missing_mlb_df, right=external_id_map, left_on=FG_ID, right_on="FanGraphsID", indicator=True, how="left")
mlb_success = mlb_merge[mlb_merge["_merge"] == "both"]
mlb_success = mlb_success[[NAME, NAME_ASCII, FG_ID, 'MLBAMID', ESPN_ID, TJ_ID]]
mlb_success.rename(columns={
  'MLBAMID': MLB_ID
}, inplace=True)
mlb_success[MLB_ID] = mlb_success[MLB_ID].astype('Int64')
# print(mlb_success.head(-25))

merged = pd.merge(mlb_success, df, left_on=TJ_ID, right_on=TJ_ID, how='outer', indicator=True)

merged[MLB_ID] = merged['mlb_id_y'].fillna(merged['mlb_id_x'])
merged = merged[['name_y', 'name_ascii_y', 'fg_id_y', MLB_ID, 'espn_id_y', TJ_ID]]
merged.rename(columns={
  'name_y': NAME,
  'name_ascii_y': NAME_ASCII,
  'fg_id_y': FG_ID,
  'espn_id_y': ESPN_ID
}, inplace=True)
print(merged.head(5))
print(df.shape)
print(merged.shape)

missing_mlb_df = mlb_merge[mlb_merge['_merge'] == 'left_only']
missing_mlb_df = missing_mlb_df[[NAME, NAME_ASCII, FG_ID, "MLBAMID", ESPN_ID, TJ_ID]]
print(missing_mlb_df.shape)

# missing_mlb_df.to_csv('../output_to_process/missing_mlb_id.csv')
# merged.to_csv('../output_final/tj_id_map.csv', index=False)
