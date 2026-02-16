import pandas as pd
from col_config import (
  TJ_ID,
  C,
  FIRST,
  SECOND,
  THIRD,
  SS,
  OF,
  SP,
  RP,
  UTIL
)


df = pd.read_csv('../output_to_process/elig.csv')
df.rename(columns={
  'tjid': TJ_ID,
  'C': C,
  '1B': FIRST,
  '2B': SECOND,
  '3B': THIRD,
  'SS': SS,
  'OF': OF,
  'Util': UTIL,
  'SP': SP,
  'RP': RP
}, inplace=True)

df = df[[TJ_ID, C, FIRST, SECOND, SS, THIRD, OF, UTIL, SP, RP]]
df.to_csv("../output_final/elig.csv", index=False)

