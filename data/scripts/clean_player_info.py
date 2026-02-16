import pandas as pd
from col_config import (
  TJ_ID,
  FG_ID,
  PLAYER_MLB_ORG,
  PLAYER_POS,
  PLAYER_AGE,
  PLAYER_JERSEY
)

df = pd.read_csv('../output_to_process/player_info.csv')
df.rename(columns={
  'tjid': TJ_ID,
  'fgId': FG_ID,
  'org': PLAYER_MLB_ORG,
  'pos': PLAYER_POS,
  'age': PLAYER_AGE,
  'jersey': PLAYER_JERSEY
}, inplace=True)

df[PLAYER_JERSEY] = df[PLAYER_JERSEY].astype('Int64')
df = df[[TJ_ID, PLAYER_MLB_ORG, PLAYER_POS, PLAYER_AGE, PLAYER_JERSEY]]
df.to_csv('../output_final/player_info.csv', index=False)
