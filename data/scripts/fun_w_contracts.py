import pandas as pd

contracts = pd.read_csv('./contracts_final.csv',)
contracts.drop(columns=['Unnamed: 0'], inplace=True)
# print(contracts.head(20))

# aaa_opts = contracts[(contracts['aaa_options']) & (contracts['team_id'] == 19)]
aaa_opts = contracts[(contracts['aaa_options']) & (contracts['team_id'] == 9)]
# aaa_opts = contracts[contracts['aaa_options']]
print(aaa_opts.head(7))