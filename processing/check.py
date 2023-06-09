import pandas as pd

def check(filename):

    # Step 1: Read the target.csv file into a Pandas DataFrame
    target_df = pd.read_csv(f'./processed/{filename}.csv', encoding='utf-8-sig')

    # Step 2: Read the korail.csv file into a Pandas DataFrame
    korail_df = pd.read_csv('./processed/korail.csv', encoding='utf-8-sig')

    # Step 3: Extract the values of the first column of each DataFrame
    target_values = target_df.iloc[:, 0]

    korail_values = korail_df.iloc[:, 0]

    not_in_korail = target_values[~target_values.isin(korail_values)]
    if len(not_in_korail) == 0:
        print(f"All {filename}.csv are in korail.csv")
    else:
        print(not_in_korail)

    not_in_korail = korail_values[~korail_values.isin(target_values)]
    if len(not_in_korail) == 0:
        print(f"All korail.csv are in {filename}.csv")
    else:
        print(not_in_korail)