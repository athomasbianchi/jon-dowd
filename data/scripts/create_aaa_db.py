import pandas as pd

contracts = pd.read_csv('../output_final/contracts.csv')
aaa_db = contracts[contracts['aaa_options'] == True]
aaa_db = aaa_db[['contract_id', 'tj_id', 'team_id']]
aaa_db['picked_up'] = None

print(aaa_db.head())

aaa_db.to_csv('../output_final/aaa_26.csv', index=False)

