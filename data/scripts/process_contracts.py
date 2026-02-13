import pandas as pd

contracts = pd.read_csv("./contracts_raw_w_namefixes.csv")
contracts_process = contracts.drop(columns=["Position"])


# types
def set_type(row):
    if row["Years"] == "Arb 1" or row["Years"] == "Arb 2" or row["Years"] == "Arb 3":
        return row["Years"]
    elif row["League"] == "Cut":
        return "cut"
    elif row["Years"] == "U":
        return "aa"
    elif row["Symbol"] == "@":
        return "pre-arb"
    elif str(row["Symbol"]).startswith("@"):
        return "pre-arb"
    elif row["Symbol"] == "†":
        return "aaa option"
    elif row["Dollars"].startswith("$"):
        return "contract"
    else:
        return None


# add type
contracts_process["type"] = contracts_process.apply(set_type, axis=1)
contracts_process["Player"] = contracts_process.apply(
    lambda row: row["Player"].replace("©", ""), axis=1
)
contracts_process["Player"] = contracts_process.apply(
    lambda row: row["Player"].rstrip(), axis=1
)


# print(contracts_process.head(50))
# print(contracts_process[contracts_process['type'] == None])

players = pd.read_csv("../id_map/tj_id_map.csv")
# print(players.head(10))
players_to_merge = players[["NameASCII", "espnId", "fgId", "tjid"]]
# print(players_to_merge.head(50))

contracts_process = pd.merge(
    contracts_process,
    players_to_merge,
    how="left",
    left_on="Player",
    right_on="NameASCII",
    indicator=True,
)
print(contracts_process.head(50))

contracts_output = contracts_process[
    [
        "Original Team",
        "NameASCII",
        "fgId",
        "tjid",
        "type",
        "Years",
        "Dollars",
        "Symbol",
        "Options",
    ]
]

contracts_output["dup"] = contracts_output.duplicated(subset=["NameASCII"])
# contracts_df = contracts_output[contracts_output['dup'] == False]

# add team_id
team_df = pd.read_csv("../output/teams.csv")
team_merge = team_df[["name", "id"]]
team_merge.rename(columns={"name": "Original Team", "id": "team_id"}, inplace=True)
contracts_output["Original Team"] = contracts_output["Original Team"].replace(
    "Cheating Raiders", "The Cheating Raiders"
)
contracts = pd.merge(
    left=contracts_output,
    right=team_merge,
    on="Original Team",
    how="left",
)
contracts = contracts[
    [
        "Original Team",
        "team_id",
        "NameASCII",
        "tjid",
        "fgId",
        "type",
        "Years",
        "Dollars",
        "Symbol",
        "Options",
        "dup",
    ]
]

# clean $
contracts.rename(columns={"Dollars": "dollars"}, inplace=True)
non_dollar_types = ["aaa option", "Arb 1", "Arb 2", "Arb 3", "aa"]
contracts["dollars"] = contracts.apply(
    lambda row: "$0" if row["type"] in non_dollar_types else row["dollars"], axis=1
)
contracts["dollars"] = contracts["dollars"].apply(lambda x: x.strip("$"))
contracts["dollars"] = contracts["dollars"].astype("float")

# clean types
contracts.type.replace(
    ["aaa option", "Arb 1", "Arb 2", "Arb 3", "pre-arb"],
    ["aaa_opt", "arb1", "arb2", "arb3", "pre_arb"],
    inplace=True,
)

# clean years
contracts.rename(columns={'Years': 'years'}, inplace=True)
non_year_types = ["aaa_option", "arb1", "arb2", "arb3", "aa"]
contracts["years"] = contracts.apply(
    lambda row: None if row["type"] in non_year_types else row["years"], axis=1
)

# drop symbols
contracts.drop(columns='Symbol', inplace=True)

# options -> aa_options
contracts.rename(columns={'Options': 'aa_options'}, inplace=True)
contracts['aa_options'] = contracts["aa_options"].astype('Int64')

# add aaa_options
# aaa_opt $3
contracts['aaa_options'] = contracts.apply(lambda row: row['type'] == 'aaa_opt', axis=1)

# add arb_options
arb_map = {'arb1': .4, 'arb2': .6, 'arb3': .8}
contracts['arb_rate'] = contracts.apply(lambda row: arb_map.get(row['type']) or None, axis=1)

contracts.to_csv('./contracts_clean_w_dups.csv')
