import requests
import pandas as pd

url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/flb/seasons/2026/segments/0/leagues/12577"

querystring = {"view": "kona_player_info"}

headers = {
    "x-fantasy-filter": '{"players": {"limit": 4000,"sortDraftRanks": {"sortPriority": 100,"sortAsc": true, "value": "STANDARD"}}}'
}


response = requests.get(url, headers=headers, params=querystring)
data = response.json()
players = data["players"]

def get_espn_proj(player):
  id = player['id']
  name = player['player']['fullName']
  stats = player['player']['stats']
  # JUDGE
  # last 7/15/30 vs. pitcher tbd
  # "id": "002025", "appliedTotal": 778.0, (25 total!)
  # "id": "002026", "appliedTotal": 0.0, (26 total?)
  # "id": "032026", "appliedTotal": 0.0,
  # "id": "022026", "appliedTotal": 0.0,
  # "id": "012026", "appliedTotal": 0.0,
  # "id": "102025", "appliedTotal": 503.0, (25 projectctions)
  # "id": "102026", "appliedTotal": 776.0, (26 projections)
  proj_26 = [stat for stat in stats if stat['id'] == '102026']
  proj_total = proj_26[0]['appliedTotal'] if len(proj_26) else 0
  total_25 = [stat for stat in stats if stat['id'] == '002025']
  ly_total = total_25[0]['appliedTotal'] if len(total_25) else 0
  return {
    'id': id,
    'name': name,
    'proj_26': proj_total,
    'total_25': ly_total
  }

projections = map(get_espn_proj, players)
proj_df = pd.DataFrame(projections)
proj_df.rename(columns={'proj_26': 'proj'}, inplace=True)
proj_df.sort_values(by='proj', ascending=False, inplace=True)
proj_df["proj"] = proj_df["proj"].round(1)
proj_df['total_25'] = proj_df['total_25'].round(1)
proj_df.to_csv('./input_download/espn_proj.csv')

df = pd.json_normalize(players)
df = df[
  [
    "id",
    "player.fullName",
    "player.lastName",
    "player.defaultPositionId",
    "player.proTeamId",
    "player.jersey",
    "player.injured",
    "player.injuryStatus",
    "player.eligibleSlots",
    "player.draftRanksByRankType.STANDARD.rank",
  ]
]
df = df.rename(
  columns={
    "id": "espnId",
    "player.fullName": "fullName",
    "player.lastName": "lastName",
    "player.defaultPositionId": "DefaultPositionId",
    "player.proTeamId": "teamId",
    "player.jersey": "jersey",
    "player.injured": "injured",
    "player.injuryStatus": "injuryStatus",
    "player.eligibleSlots": "eligibleSlots",
    "player.draftRanksByRankType.STANDARD.rank": "rank",
  }
)

df.to_csv("./input_download/espn.csv")
