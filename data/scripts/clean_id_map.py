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

# todo handle fixes

missing_mlb_df.to_csv('../output_to_process/missing_mlb_id.csv')
df.to_csv('../output_final/tj_id_map.csv', index=False)