import requests
import pandas as pd

url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/flb/seasons/2026/segments/0/leagues/12577"

querystring = {"view": "mTeam"}

response = requests.get(url, params=querystring)
data = response.json()
teams = data['teams']

teams_df = pd.json_normalize(teams)
teams_df = teams_df[['abbrev', 'id', 'name']]
teams_df['level'] = teams_df.apply(lambda row: 'minors' if (row['id'] < 19 and row['id'] > 11) else 'majors', axis=1)
teams_df.rename(columns={'id': 'team_id'}, inplace=True)
teams_df = teams_df[['team_id', 'abbrev', 'name', 'level']]

teams_df.to_csv('../output/teams.csv', index=False)
