import os
import pandas as pd

os.chdir("C:\\Users\\amyes\\Box\\TxDH\\capitol_project\\data")

cards = pd.read_csv("payroll_cards_all_output.csv")
cards['first_initial'] = cards['first_name'].astype(str).str[0]
cards['last_initial'] = cards['last_name'].astype(str).str[0]
matches_col = []
matches_level = []

census = pd.read_excel("1880_Full.xlsx")
census['name'] = census['Given Name'] + " " + census['Surname']
census['first_initial'] = census['Given Name'].astype(str).str[0]
census['last_initial'] = census['Surname'].astype(str).str[0]
census['f_name'] = census['first_initial'] + " " + census['Surname']
census['l_name'] = census['Given Name'] + " " + census['last_initial']

for index, row in cards.iterrows():
    searchname = str(row['first_name']) + " " + str(row['last_name'])
    match_score = 0
    matches = census.loc[census['name'] == searchname]
    num_exact = len(matches)
    if num_exact > 0:
        index_list = list(matches.index.values)
        match_details = ', '.join(str(x) for x in index_list)
        match_level = 1
    else:
        searchname = str(row['first_initial']) + " " + str(row['last_name'])
        matches = census.loc[census['f_name'] == searchname]
        num_exact = len(matches)
        if num_exact > 0:
            index_list = list(matches.index.values)
            match_details = ', '.join(str(x) for x in index_list)
            match_level = 2
        else:
            searchname = str(row['first_name']) + " " + str(row['last_initial'])
            matches = census.loc[census['l_name'] == searchname]
            num_exact = len(matches)
            if num_exact > 0:
                index_list = list(matches.index.values)
                match_details = ', '.join(str(x) for x in index_list)
                match_level = 3
            else:
                match_details = "No potential matches."
                match_level = 4
    
    matches_col.append(match_details)
    matches_level.append(match_level)
    print(match_details)
    

cards['Matches'] = matches_col
cards['Match Level'] = matches_level
cards.to_excel("cards_matches.xlsx")
