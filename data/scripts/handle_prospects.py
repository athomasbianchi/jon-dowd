import pandas as pd

comp_df = pd.read_csv("../input_download/2026_comp_prospects.csv")
comp_df["mlbam"] = comp_df["mlbam"].astype("Int64")
id_map = pd.read_csv("../output_final/tj_id_map.csv")
id_map["mlb_id"] = id_map["mlb_id"].astype("Int64")

merged_df = pd.merge(
    left=comp_df,
    right=id_map,
    left_on="mlbam",
    right_on="mlb_id",
    how="left",
    indicator=True,
)

df = merged_df[
    [
        "Name",
        "Team",
        "Pos",
        "Age",
        "Rank",
        "Avg",
        "TJStats",
        "Fangraphs",
        "mlbam",
        "fg_id",
        "espn_id",
        "tj_id",
        "name",
        "name_ascii",
    ]
]
has_fg_id = df[~df["fg_id"].isna()]
has_fg_id = has_fg_id[
    [
        "name",
        "Team",
        "Pos",
        "Age",
        "Rank",
        "Avg",
        "TJStats",
        "Fangraphs",
        "mlbam",
        "fg_id",
        "espn_id",
        "tj_id",
    ]
]
needs_fg_id = df[df["fg_id"].isna()]


def last_first(str):
    name_list = str.split(",")
    first = name_list[1].strip()
    last = name_list[0].strip()
    return f"{first} {last}"


needs_fg_id["Name"] = needs_fg_id["Name"].apply(last_first)

name_match = pd.merge(
    left=needs_fg_id,
    right=id_map,
    how="left",
    left_on="Name",
    right_on="name_ascii",
    indicator=True,
)
has_fg_id_2 = name_match[
    [
        "Name",
        "Team",
        "Pos",
        "Age",
        "Rank",
        "Avg",
        "TJStats",
        "Fangraphs",
        "mlbam",
        "fg_id_y",
        "espn_id_y",
        "tj_id_y",
        "name_y",
        "name_ascii_y",
    ]
]
has_fg_id_2 = has_fg_id_2[
    [
        "name_y",
        "Team",
        "Pos",
        "Age",
        "Rank",
        "Avg",
        "TJStats",
        "Fangraphs",
        "mlbam",
        "fg_id_y",
        "espn_id_y",
        "tj_id_y",
    ]
]
has_fg_id_2.rename(
    columns={
        "name_y": "name",
        "fg_id_y": "fg_id",
        "espn_id_y": "espn_id",
        "tj_id_y": "tj_id",
    },
    inplace=True,
)


still_needs = name_match[name_match["_merge"] == "left_only"]
still_needs = still_needs[
    [
        "Name",
        "Team",
        "Pos",
        "Age",
        "Rank",
        "Avg",
        "TJStats",
        "Fangraphs",
        "mlbam",
        "fg_id_y",
        "espn_id_y",
        "tj_id_y",
        "name_y",
        "name_ascii_y",
    ]
]

still_needs = still_needs[
    ["Name", "Team", "Pos", "Age", "Rank", "Avg", "TJStats", "Fangraphs", "mlbam"]
]
still_needs.rename(columns={"Name": "name"}, inplace=True)

prospects = pd.concat([has_fg_id, has_fg_id_2, still_needs], ignore_index=True)
prospects.sort_values(by=["Rank"], inplace=True, ignore_index=True)
# print(prospects.head(5))

contracts = pd.read_csv("../output_final/contracts.csv")
# print(contracts.head(5))
prospects = pd.merge(
    left=prospects,
    right=contracts,
    how="left",
    left_on="tj_id",
    right_on="tj_id",
    indicator=True,
)

teams = pd.read_csv("../output_final/teams.csv")
teams = teams[["team_id", "abbrev"]]
prospects = pd.merge(
    left=prospects, right=teams, how="left", left_on="team_id", right_on="team_id"
)
prospects = prospects[
    [
        "abbrev",
        "name",
        "Team",
        "Pos",
        "Age",
        "Rank",
        "Avg",
        "TJStats",
        "Fangraphs",
    ]
]

prospects.to_csv("../output_final/prospects.csv", index=False)


# prosp_id_map = pd.read_csv("../input_custom/prosp_id_map.csv")
# prosp_id_map["mlb_id"] = prosp_id_map["mlb_id"].astype("Int64")

# custom_input = pd.merge(left=still_needs, right=prosp_id_map, how="left", left_on="mlbam", right_on="mlb_id", indicator=True)
# has_fg_id_3 = custom_input[custom_input['_merge'] == 'both']
# still_needs = custom_input[custom_input['_merge'] == 'left_only']
# has_fg_id_3 = has_fg_id_3[['Name', 'Team', 'Pos', 'Age', 'Rank', 'Avg', 'TJStats', 'Fangraphs', 'mlbam', 'fg_id',]]
# has_fg_id_3 = pd.merge(left=has_fg_id_3, right=id_map, how="left", left_on="fg_id", right_on="fg_id", indicator=True)
# # custom_input = custom_input[["Name", "Team", "Pos", "Age", "Rank", "Avg", "TJStats", "Fangraphs", "mlbam", "fg_id_y", "espn_id_y", "tj_id_y", "name_y", "name_ascii_y"]]
# print(custom_input.columns)

# still_needs.to_csv('../output_to_process/prospects_need_ids.csv', index=False)

# name_match = name_match[['Name', 'Team', 'Pos', 'Rank', 'Avg', 'TJStats', 'Fangraphs', 'mlbam', 'Age']]
