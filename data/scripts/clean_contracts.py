import pandas as pd
from col_config import (
    TEAM_ID,
    TJ_ID,
    CONTRACT_TYPE,
    CONTRACT_YEARS,
    CONTRACT_DOLLARS,
    AA_OPTIONS,
    AAA_OPTIONS,
    ARB_RATE,
    CONTRACT_ID,
)

df = pd.read_csv("../output_to_process/contracts.csv")
df.rename(
    columns={
        "tjid": TJ_ID,
        "years": CONTRACT_YEARS,
        "type": CONTRACT_TYPE,
        "dollars": CONTRACT_DOLLARS,
    },
    inplace=True,
)
df = df[
    [
        TEAM_ID,
        TJ_ID,
        CONTRACT_TYPE,
        CONTRACT_YEARS,
        CONTRACT_DOLLARS,
        AA_OPTIONS,
        AAA_OPTIONS,
        ARB_RATE,
    ]
]

# add contract_ids
# contracted players
contract_df = df[df[CONTRACT_TYPE] == "contract"]
contract_df.sort_values(
    by=[CONTRACT_YEARS], ascending=False, inplace=True, ignore_index=True
)
contract_df[CONTRACT_ID] = contract_df.index.to_series().apply(
    lambda x: f"25_con_{x + 1}"
)

# aaa players
aaa_df = df[df[CONTRACT_TYPE] == "aaa_opt"]
aaa_df.reset_index(inplace=True, drop=True)
aaa_df[CONTRACT_ID] = aaa_df.index.to_series().apply(lambda x: f"25_aaa_{x+1}")

# aa players
aa_df = df[df[CONTRACT_TYPE] == "aa"]
aa_df.reset_index(inplace=True, drop=True)
aa_df[CONTRACT_ID] = aa_df.index.to_series().apply(lambda x: f"25_aa_{x+1}")

# cut players
cut_df = df[df[CONTRACT_TYPE] == "cut"]
cut_df.reset_index(inplace=True, drop=True)
cut_df[CONTRACT_ID] = cut_df.index.to_series().apply(lambda x: f"25_cut_{x+1}")

# pre-arb
pre_arb_df = df[df[CONTRACT_TYPE] == "pre_arb"]
pre_arb_df.reset_index(inplace=True, drop=True)
pre_arb_df[CONTRACT_ID] = pre_arb_df.index.to_series().apply(
    lambda x: f"25_prearb_{x+1}"
)

# arb
arb_df = df.loc[df[CONTRACT_TYPE].isin(["arb1", "arb2", "arb3"])]
arb_df.sort_values(by=CONTRACT_TYPE, ascending=False, inplace=True, ignore_index=True)
arb_df[CONTRACT_ID] = arb_df.index.to_series().apply(lambda x: f"25_arb_{x+1}")

# combine types
export_df = pd.concat(
    [contract_df, aaa_df, aa_df, cut_df, pre_arb_df, arb_df], ignore_index=True
)
export_df = export_df[
    [
        CONTRACT_ID,
        TJ_ID,
        TEAM_ID,
        CONTRACT_TYPE,
        CONTRACT_YEARS,
        CONTRACT_DOLLARS,
        AA_OPTIONS,
        AAA_OPTIONS,
        ARB_RATE,
    ]
]
export_df.to_csv("../output_final/contracts.csv", index=False)
