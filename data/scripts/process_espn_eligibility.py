import pandas as pd
import json

df = pd.read_csv("../input_download/espn.csv")

PRO_TEAM_IDS = {
    0: "FA",
    1: "BAL",
    2: "BOS",
    3: "LAA",
    4: "CHW",
    5: "CLE",
    6: "DET",
    7: "KCR",
    8: "MIL",
    9: "MIN",
    10: "NYY",
    11: "ATH",
    12: "SEA",
    13: "TEX",
    14: "TOR",
    15: "ATL",
    16: "CHC",
    17: "CIN",
    18: "HOU",
    19: "LAD",
    20: "WSN",
    21: "NYM",
    22: "PHI",
    23: "PIT",
    24: "STL",
    25: "SDP",
    26: "SFG",
    27: "COL",
    28: "MIA",
    29: "ARI",
    30: "TBR",
}

DEF_POS_MAP = {
    1: "SP",
    2: "C",
    3: "1B",
    4: "2B",
    5: "3B",
    6: "SS",
    7: "OF",
    8: "OF",
    9: "OF",
    10: "DH",
    11: "RP",
}

# SLOTS
# 0 C
# 1 1B
# 2 2B
# 3 3B
# 4 SS
# 5 OF
# 6 MI
# 7 CI
# 8 LF
# 9 CF
# 10 RF
# 11 DH
# 12 UTIL
# 13 P
# 14 SP
# 15 RP
# 16 BE?
# 17 BE? / IL ?
# 19 IF

df["rank"] = df["rank"].astype("Int64")
df["jersey"] = df["jersey"].astype("Int64")
df["org"] = df["teamId"].apply(lambda x: PRO_TEAM_IDS[x])
df["C"] = df["eligibleSlots"].apply(lambda x: 0 in json.loads(x))
df["1B"] = df["eligibleSlots"].apply(lambda x: 1 in json.loads(x))
df["2B"] = df["eligibleSlots"].apply(lambda x: 2 in json.loads(x))
df["3B"] = df["eligibleSlots"].apply(lambda x: 3 in json.loads(x))
df["SS"] = df["eligibleSlots"].apply(lambda x: 4 in json.loads(x))
df["OF"] = df["eligibleSlots"].apply(lambda x: 5 in json.loads(x))
df["Util"] = df["eligibleSlots"].apply(
    lambda x: any(num in [0, 1, 2, 3, 4, 5, 11] for num in json.loads(x))
)
df["SP"] = df["eligibleSlots"].apply(lambda x: 14 in json.loads(x))
df["RP"] = df["eligibleSlots"].apply(lambda x: 15 in json.loads(x))

print(df.head(5))

# Add tjid from id_map
id_map = pd.read_csv("../output/tj_id_map.csv")
id_map["espnId"] = id_map["espnId"].astype("Int64")
id_map["MLBAMID"] = id_map["MLBAMID"].astype("Int64")

e_pos = pd.merge(left=df, right=id_map, how="left", on="espnId")

# exclude players w/o tjid
e_pos = e_pos[~e_pos["tjid"].isna()]
errors = e_pos[e_pos["tjid"].isna()]
errors = errors[
    [
        "fullName",
        "org",
        "espnId",
        "rank",
    ]
]
errors.to_csv("elig_err.csv", index=False)

e_pos = e_pos[
    [
        "tjid",
        "fgId",
        "MLBAMID",
        "espnId",
        "NameASCII",
        "C",
        "1B",
        "2B",
        "SS",
        "3B",
        "OF",
        "Util",
        "SP",
        "RP",
    ]
]
e_pos.to_csv("../output/elig.csv", index=False)
