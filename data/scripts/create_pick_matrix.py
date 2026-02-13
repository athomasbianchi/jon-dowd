import pandas as pd
import math
import numbers

# 0      CR   1  The Cheating Raiders  majors
# 1      SF   2        Structure Fire  majors
# 2      BS   3        Bayou Shooters  majors
# 3      RW   4            Ryno World  majors
# 4     DET   5  Detroit Nittany Tide  majors
# 5     ORl   6     Orlando Renegades  majors
# 6      SZ   7   Springfield Zephyrs  majors
# 7     DCT   8      Dip City Thunder  majors
# 8      YB   9           Young Bucks  majors
# 9      CS  10        Country Strong  majors
# 16     MJ  19       Midtown Jaguars  majors
# 17    WCS  20   West Coast Spartans  majors

AA_ROUNDS = 15
TEAM_IDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 19, 20]
ORDER = {19: 1, 6: 2, 20: 3, 2: 4, 4: 5, 3: 6, 5: 7, 7: 8, 10: 9, 9: 10, 1: 11, 8: 12}

TEAM_ABBREVS = {
    1: "CR",
    2: "SF",
    3: "BS",
    4: "RW",
    5: "DET",
    6: "ORl",
    7: "SZ",
    8: "DCT",
    9: "YB",
    10: "CS",
    19: "MJ",
    20: "WCS",
}

dpm_26_df = pd.DataFrame(
    columns=[
        "pick_id",
        "year",
        "round",
        "original_team_id",
        "picking_team_id",
        "overall_pick",
        "player_id",
        "available_slot",
    ]
)


def gen_team_picks_df(team_id):
    team_dict = {
        "original_team_id": [],
        "round": [],
    }
    for i in range(AA_ROUNDS):
        round = i + 1
        team_dict["original_team_id"].append(team_id)
        team_dict["round"].append(round)
    df = pd.DataFrame(team_dict)
    return df


for team_id in TEAM_IDS:
    team_dict = gen_team_picks_df(team_id)
    dpm_26_df = pd.concat([dpm_26_df, team_dict], ignore_index=True)

dpm_26_df["year"] = 2026
dpm_26_df["order"] = dpm_26_df["original_team_id"].apply(lambda x: ORDER[x])
dpm_26_df["original_team_abbr"] = dpm_26_df["original_team_id"].apply(
    lambda x: TEAM_ABBREVS[x].lower()
)
dpm_26_df = dpm_26_df.sort_values(by=["round", "order"], ignore_index=True)
dpm_26_df["pick_id"] = dpm_26_df.apply(
    lambda row: f"{row['year']}_{row['original_team_abbr'].lower()}_{row['round']}",
    axis=1,
)

# dpm_26_df.sort_values(by=[])
print(dpm_26_df)

# add trades
trades_df = pd.read_csv("./trades.csv")
dpm_26_df = pd.merge(left=dpm_26_df, right=trades_df, on="pick_id", how="outer")
dpm_26_df["team_id"] = dpm_26_df["team_id"].astype("Int64")
dpm_26_df.drop(columns=["picking_team_id", "abbr"], inplace=True)
dpm_26_df.rename(columns={"team_id": "traded_team_id"}, inplace=True)
dpm_26_df = dpm_26_df.sort_values(by=["round", "order"], ignore_index=True)
dpm_26_df["traded_team_abbr"] = dpm_26_df["traded_team_id"].apply(
    lambda x: None if math.isnan(x) else TEAM_ABBREVS[x].lower()
)

dpm_26_df["picking_team_id"] = dpm_26_df.apply(
    lambda row: row["traded_team_id"] if isinstance(row["traded_team_id"], numbers.Number) else row["original_team_id"],
    axis=1,
)
dpm_26_df["picking_team_abbr"] = dpm_26_df['picking_team_id'].apply(
    lambda x: None if math.isnan(x) else TEAM_ABBREVS[x].lower()
)

dpm_26_df = dpm_26_df[['pick_id', 'year', 'round', 'order', 'picking_team_id', 'picking_team_abbr', 'original_team_id', 'original_team_abbr', 'traded_team_id', 'traded_team_abbr']]
print(dpm_26_df.head(24))
# print(dpm_26_df[dpm_26_df['picking_team_id'] == 9].head(15))
dpm_26_df.to_csv('../output/draft.csv', index=False)