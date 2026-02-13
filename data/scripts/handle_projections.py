import pandas as pd

# Batting
# Runs Scored (R)1
# Singles (1B)1
# Doubles (2B)2
# Triples (3B)3
# Home Runs (HR)4
# Runs Batted In (RBI)1
# Walks (BB)1
# Hit by Pitch (HBP)1
# Stolen Bases (SB)2

# Pitching
# Innings Pitched (IP)2
# Hits Allowed (H)-0.5
# Earned Runs (ER)-1
# Walks Issued (BB)-0.5
# Hit Batsmen (HB)-0.5
# Strikeouts (K)1
# Complete Games (CG)5
# Wins (W)10
# Saves (SV)10

pd.options.display.float_format = "{:.2f}".format

atc_h = pd.read_csv("../input_download/2026_atc_h.csv")
atc_h["fp"] = (
    atc_h["1B"]
    + atc_h["2B"] * 2
    + atc_h["3B"] * 3
    + atc_h["HR"] * 4
    + atc_h["R"]
    + atc_h["RBI"]
    + atc_h["BB"]
    + atc_h["SB"] * 2
)
atc_h = atc_h[["NameASCII", "PlayerId", "G", "PA", "fp"]]
atc_h["fp/g"] = atc_h["fp"] / atc_h["G"]
atc_h["fp/pa"] = atc_h["fp"] / atc_h["PA"]
atc_h.sort_values(by="fp/g", ascending=False, inplace=True)

batx_h = pd.read_csv("../input_download/2026_batx_h.csv")
batx_h["fp"] = (
    batx_h["1B"]
    + batx_h["2B"] * 2
    + batx_h["3B"] * 3
    + batx_h["HR"] * 4
    + batx_h["R"]
    + batx_h["RBI"]
    + batx_h["BB"]
    + batx_h["SB"] * 2
)
batx_h = batx_h[["NameASCII", "PlayerId", "G", "PA", "fp"]]
batx_h["fp/g"] = batx_h["fp"] / batx_h["G"]
batx_h["fp/pa"] = batx_h["fp"] / batx_h["PA"]
batx_h.sort_values(by="fp/g", ascending=False, inplace=True)

atc_p = pd.read_csv("../input_download/2026_atc_p.csv")
atc_p["fp"] = (
    atc_p["IP"] * 2
    + atc_p["H"] * -0.5
    + atc_p["ER"] * -1
    + atc_p["BB"] * -0.5
    + atc_p["HBP"] * -0.5
    + atc_p["SO"]
    + atc_p["W"] * 10
    + atc_p["SV"] * 10
)
atc_p = atc_p[["NameASCII", "PlayerId", "G", "GS", "fp"]]
atc_p["fp/g"] = atc_p["fp"] / atc_p["G"]
atc_p["fp/gs"] = atc_p["fp"] / atc_p["GS"]
atc_p.sort_values(by="fp", ascending=False, inplace=True)
# print(atc_p.head(20))

oopsy_p = pd.read_csv("../input_download/2026_oopsy_p.csv")
oopsy_p["fp"] = (
    oopsy_p["IP"] * 2
    + oopsy_p["H"] * -0.5
    + oopsy_p["ER"] * -1
    + oopsy_p["BB"] * -0.5
    + oopsy_p["HBP"] * -0.5
    + oopsy_p["SO"]
    + oopsy_p["W"] * 10
    + oopsy_p["SV"] * 10
)
oopsy_p = oopsy_p[["NameASCII", "PlayerId", "G", "GS", "fp"]]
oopsy_p["fp/g"] = oopsy_p["fp"] / oopsy_p["G"]
oopsy_p["fp/gs"] = oopsy_p["fp"] / oopsy_p["GS"]
oopsy_p.sort_values(by="fp", ascending=False, inplace=True)

p = pd.merge(
    left=atc_p,
    right=oopsy_p,
    on="PlayerId",
    how="outer",
    indicator=True,
    suffixes=["_atc", "_oopsy"],
)
p["dif"] = p["fp_oopsy"] - p["fp_atc"]
p = p[["NameASCII_oopsy", "PlayerId", "fp_atc", "fp_oopsy", "dif"]]
p.rename(columns={"NameASCII_oopsy": "NameASCII", "fp_oopsy": "fp_alt"}, inplace=True)
p["fp_avg"] = (p["fp_atc"] + p["fp_alt"]) / 2
p.sort_values("fp_avg", ascending=False, inplace=True)

h = pd.merge(
    left=atc_h,
    right=batx_h,
    on="PlayerId",
    how="outer",
    indicator=True,
    suffixes=["_atc", "_batx"],
)
h["dif"] = h["fp_batx"] - h["fp_atc"]
h = h[["NameASCII_batx", "PlayerId", "fp_atc", "fp_batx", "dif"]]
h.rename(columns={"NameASCII_batx": "NameASCII", "fp_batx": "fp_alt"}, inplace=True)
h["fp_avg"] = (h["fp_atc"] + h["fp_alt"]) / 2
h.sort_values("fp_avg", ascending=False, inplace=True)

players = pd.concat([p, h])
players.sort_values(by="fp_avg", ascending=False, inplace=True)
players = players.groupby("PlayerId").sum().reset_index()
players.sort_values(by="fp_avg", ascending=False, inplace=True)

# add tj_id & espnId
player_map = pd.read_csv('../output/tj_id_map.csv')
player_map[["MLBAMID", "espnId"]] = player_map[["MLBAMID", "espnId"]].astype('Int64')
proj_w_ids = pd.merge(left=players, right=player_map, left_on='PlayerId', right_on='fgId', indicator=True, how='inner')
proj_w_ids = proj_w_ids[['tjid', 'fgId', 'espnId', 'NameASCII_y', 'fp_atc', 'fp_alt', 'dif', 'fp_avg']]
proj_w_ids.rename(columns={'NameASCII_y': 'NameASCII'}, inplace=True)

# add espn projections by espn Id
espn_proj = pd.read_csv('../input_download/espn_proj.csv')
proj_all = pd.merge(how='inner', left=proj_w_ids, right=espn_proj, left_on='espnId', right_on='id')
proj_all = proj_all[['tjid', 'fgId', 'espnId', 'NameASCII', 'fp_atc', 'fp_alt', 'dif', 'fp_avg', 'proj']]
proj_all.rename(columns={'proj': 'fp_e', 'dif': 'alt-atc'}, inplace=True)
proj_all['atc-e'] = proj_all['fp_atc'] - proj_all['fp_e']
proj_all.sort_values(by='fp_avg', ascending=False, inplace=True)

proj_all.to_csv('../output/projections.csv')