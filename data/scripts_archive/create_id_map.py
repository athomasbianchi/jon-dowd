import pandas as pd
import re
from unidecode import unidecode
import string


# start with known dupes / fixes
dup_df = pd.read_csv("../input_custom/dupes_fixed.csv")
loser_df = pd.read_csv("../input_custom/losers.csv")
name_fix_df = pd.read_csv("../input_custom/name_fixes.csv")
dup_df = dup_df[["Name", "NameASCII", "fgId", "MLBAMID", "espnId"]]
dup_df["espnId"] = dup_df["espnId"].astype("Int64")
loser_df["NameASCII"] = loser_df["Name"]
name_fix_df["NameASCII"] = name_fix_df["fullName"]
name_fix_df["Name"] = name_fix_df["fullName"]
name_fix_df = name_fix_df[["Name", "NameASCII", "fgId", "espnId"]]
preload_df = pd.concat([dup_df, loser_df, name_fix_df], ignore_index=True)
preload_df["fgId"] = preload_df["fgId"].astype("string")


def remove_korean_chars(text):
    # Regex pattern to match all Hangul characters (AC00–D7A3, Hangul Syllables)
    # The 'r' before the string indicates a raw string
    korean_pattern = re.compile(r"[\uac00-\ud7a3]+")

    # Replace the matched Korean characters with an empty string
    clean_text = korean_pattern.sub("", text)
    clean_text = clean_text.rstrip()

    return clean_text


# add fangraphs mlb hitters 2024 and 2025 (two seasons)
h_24_df = pd.read_csv("../input_download/2024_mlb_h.csv")
h_25_df = pd.read_csv("../input_download/2025_ages_h.csv")
p_24_df = pd.read_csv("../input_download/2024_mlb_p.csv")
p_25_df = pd.read_csv("../input_download/2025_ages_p.csv")
h_24_df = h_24_df[["Name", "NameASCII", "PlayerId", "MLBAMID"]]
h_25_df = h_25_df[["Name", "NameASCII", "PlayerId", "MLBAMID"]]
p_24_df = p_24_df[["Name", "NameASCII", "PlayerId", "MLBAMID"]]
p_25_df = p_25_df[["Name", "NameASCII", "PlayerId", "MLBAMID"]]

# add intl players
p_kbo_df = pd.read_csv("../input_download/2025_kbo_p.csv")
h_kbo_df = pd.read_csv("../input_download/2025_kbo_h.csv")
p_npb_df = pd.read_csv("../input_download/2025_npb_p.csv")
h_npb_df = pd.read_csv("../input_download/2025_npb_h.csv")
intl_df = pd.concat([p_kbo_df, h_kbo_df, p_npb_df, h_npb_df])
intl_df = intl_df[["Name", "NameASCII", "PlayerId", "MLBAMID"]]
intl_df["Name"] = intl_df.apply(lambda row: remove_korean_chars(row["Name"]), axis=1)

# add prospects from fg
fg_prosp_df = pd.read_csv("../input_download/2025_prospects.csv")
fg_prosp_df = fg_prosp_df[["Name", "PlayerId"]]
fg_prosp_df["NameASCII"] = fg_prosp_df.apply(lambda row: unidecode(row["Name"]), axis=1)

# add college players from fg
h_ncaa_df = pd.read_csv("../input_download/2025_ncaa_h.csv")
p_ncaa_df = pd.read_csv("../input_download/2025_ncaa_p.csv")
ncaa_df = pd.concat([h_ncaa_df, p_ncaa_df])
ncaa_df = ncaa_df[["Name", "NameASCII", "PlayerId", "MLBAMID"]]

# add aaa players from fg
aaa_h_intl = pd.read_csv("../input_download/aaa_h_il.csv")
aaa_h_pcl = pd.read_csv("../input_download/aaa_h_pcl.csv")
aaa_p_intl = pd.read_csv("../input_download/aaa_p_il.csv")
aaa_p_pcl = pd.read_csv("../input_download/aaa_p_pcl.csv")

aaa_df = pd.concat([aaa_h_intl, aaa_h_pcl, aaa_p_intl, aaa_p_pcl], ignore_index=True)
aaa_df = aaa_df[
    [
        "Name",
        "PlayerId",
    ]
]
aaa_df["NameASCII"] = aaa_df["Name"]

# combine all fg inputs
fg_df = pd.concat(
    [h_25_df, p_25_df, h_24_df, p_24_df, fg_prosp_df, aaa_df, intl_df, ncaa_df],
    ignore_index=True,
)
fg_df["MLBAMID"] = fg_df["MLBAMID"].astype(
    "Int64"
)  # nullable integer for missing MLBAMIDS
fg_df["PlayerId"] = fg_df["PlayerId"].astype("string")
fg_df.drop_duplicates(
    subset=["PlayerId"], inplace=True, keep="first"
)  # keep highest source
fg_df.rename(columns={"PlayerId": "fgId"}, inplace=True)

# add fg to preloaded ID map
combined = pd.concat([preload_df, fg_df], ignore_index=True)
combined.drop_duplicates(subset=["fgId"], inplace=True, keep="first")
id_map = combined.sort_values(
    "fgId",
    ascending=True,
    ignore_index=True,
)

id_map["MLBAMID"] = id_map["MLBAMID"].astype(
    "Int64"
)  # nullable integer for missing MLBAMIDS
id_map["espnId"] = id_map["espnId"].astype(
    "Int64"
)  # nullable integer for missing espnIds
id_map = id_map[["Name", "NameASCII", "fgId", "MLBAMID", "espnId"]]

# split existing id_map into df with and with espn id
needs_eid = id_map[id_map["espnId"].isna()]
has_eid = id_map[~id_map["espnId"].isna()]

# get espn data into dataframe, just use Name and espnId
e_4k = pd.read_csv("../input_download/espn.csv")
e_ids = e_4k[["espnId", "fullName"]]

print(e_ids[e_ids["fullName"] == "Cody Ponce"])

# Marege espn data with names that need espn id on simplified name
merge = pd.merge(
    needs_eid,
    e_ids,
    how="outer",
    left_on="NameASCII",
    right_on="fullName",
    indicator=True,
)
merge_success = merge[merge["_merge"] == "both"]
merge_success["espnId"] = merge_success["espnId_y"].astype("Int64")
merge_success = merge_success[["Name", "NameASCII", "fgId", "MLBAMID", "espnId"]]
# print(merge_success[merge_success["espnId"] == 41044])
# print(merge_success[merge_success["NameASCII"] == "Julio Rodriguez"])

merge_espn_dups = merge_success[merge_success.duplicated(subset=["espnId"], keep=False)]
merge_fg_dups = merge_success[merge_success.duplicated(subset=["fgId"], keep=False)]
print(merge_espn_dups.shape)
print(merge_espn_dups.head(37))
print(merge_fg_dups.shape)
print(merge_fg_dups.head(35))
dups_to_fix = pd.concat([merge_fg_dups, merge_espn_dups])
dups_to_fix.sort_values(by="NameASCII", inplace=True)
dups_to_fix.to_csv("to_fix_dupes.csv")

dups_sorted = pd.merge(
    left=dups_to_fix, right=preload_df, how="left", on="fgId", indicator=True
)
dups_sorted.to_csv("to_fix_dupes.csv")


espn_merge = merge_success[~merge_success.duplicated(subset=["espnId"], keep=False)]
# print(espn_merge.shape)

# # remove players that already have espn id
espn_merge = pd.merge(espn_merge, has_eid, how="left", on="espnId", indicator=True)
espn_merge = espn_merge[espn_merge["_merge"] == "left_only"]
espn_merge = espn_merge[["Name_x", "NameASCII_x", "fgId_x", "MLBAMID_x", "espnId"]]
espn_merge.rename(
    columns={
        "Name_x": "Name",
        "NameASCII_x": "NameASCII",
        "fgId_x": "fgId",
        "MLBAMID_x": "MLBAMID",
    },
    inplace=True,
)

# combine existing players with espnid with new list
eid = pd.concat([has_eid, espn_merge], ignore_index=True)
eid = eid.sort_values("espnId", ignore_index=True)
# combine
id_map = pd.concat([eid, id_map], ignore_index=True)
id_map.drop_duplicates(subset=["fgId"], keep="first", inplace=True)
id_map = id_map[~id_map["fgId"].isna()]


espn_no_match = merge[merge["_merge"] == "right_only"]
espn_no_match["espnId_y"] = espn_no_match["espnId_y"].astype("Int64")
espn_no_match.rename(columns={"espnId_y": "espnId"}, inplace=True)
espn_no_match = espn_no_match[["fullName", "espnId"]]
eid_rnks = pd.read_csv("../input_download/espn.csv")
espn_no_match = pd.merge(espn_no_match, eid_rnks, how="left", on="espnId")
espn_no_match.sort_values(by=["rank"], ascending=True, inplace=True)
# print(espn_no_match.head(25))
# merge with original uploads and discard "both"
espn_to_fix = pd.merge(espn_no_match, has_eid, how="left", on="espnId", indicator=True)
espn_to_fix = espn_to_fix[espn_to_fix["_merge"] == "left_only"]
espn_to_fix.rename(columns={"fullName_x": "fullName"}, inplace=True)
espn_to_fix = espn_to_fix[["fullName", "espnId"]]
# export list to lookup
espn_to_fix.to_csv("to_find_espn.csv", index=False)


def remove_punctuation_and_whitespace(text):
    # Create a translation table to remove all punctuation
    # and all whitespace characters.
    translator = str.maketrans("", "", string.punctuation + string.whitespace)
    # Apply the translation table to the text
    cleaned_text = text.translate(translator)
    return cleaned_text


id_map["MLBAMID"] = id_map["MLBAMID"].astype("Int64")
id_map["espnId"] = id_map["espnId"].astype("Int64")
id_map["tjid"] = id_map.apply(
    lambda row: remove_punctuation_and_whitespace(row["NameASCII"]).lower(), axis=1
)

id_map_wo_dups = id_map.drop_duplicates(subset=["tjid"], keep="first")
dups_to_fix = pd.merge(id_map, id_map_wo_dups, how="left", indicator=True)
dups_to_fix = dups_to_fix[dups_to_fix["_merge"] == "left_only"]
dups_fixed = dups_to_fix[["Name", "NameASCII", "fgId", "MLBAMID", "espnId", "tjid"]]
dups_fixed["tjid"] = dups_to_fix.apply(lambda row: row["tjid"] + "1", axis=1)

id_map = pd.concat([id_map_wo_dups, dups_fixed], ignore_index=True)

id_map["dup_id"] = id_map.duplicated(subset=["tjid"])
id_map_wo_dups = id_map.drop_duplicates(subset=["tjid"], keep="first")
dups_to_fix = pd.merge(id_map, id_map_wo_dups, how="left", indicator=True)
dups_to_fix = dups_to_fix[dups_to_fix["_merge"] == "left_only"]
dups_fixed = dups_to_fix[["Name", "NameASCII", "fgId", "MLBAMID", "espnId", "tjid"]]
dups_fixed["tjid"] = dups_to_fix.apply(lambda row: row["tjid"][:-1] + "2", axis=1)

id_map = pd.concat([id_map_wo_dups, dups_fixed], ignore_index=True)

id_map["dup_id"] = id_map.duplicated(subset=["tjid"])
id_map_wo_dups = id_map.drop_duplicates(subset=["tjid"], keep="first")
dups_to_fix = pd.merge(id_map, id_map_wo_dups, how="left", indicator=True)
dups_to_fix = dups_to_fix[dups_to_fix["_merge"] == "left_only"]
dups_fixed = dups_to_fix[["Name", "NameASCII", "fgId", "MLBAMID", "espnId", "tjid"]]
dups_fixed["tjid"] = dups_to_fix.apply(lambda row: row["tjid"][:-1] + "3", axis=1)

id_map = pd.concat([id_map_wo_dups, dups_fixed], ignore_index=True)
id_map = id_map[["Name", "NameASCII", "fgId", "MLBAMID", "espnId", "tjid"]]
id_map.to_csv("../output/tj_id_map.csv", index=False)

to_find_mlbamid = id_map[id_map['MLBAMID'].isna()]
to_find_mlbamid = pd.merge(left=to_find_mlbamid, right=e_4k, on='espnId', how='left', indicator=True)
to_find_mlbamid.sort_values(by=['rank'], ignore_index=True, inplace=True)
to_find_mlbamid = to_find_mlbamid[["Name", "NameASCII", "fgId", "MLBAMID", "espnId", "tjid", 'rank']]
to_find_mlbamid.to_csv('./to_find_mlbamid.csv', index=False)
