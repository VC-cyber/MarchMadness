import pandas as pd
import numpy as np
# Load the data
team_stats_df = pd.read_csv('/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/scraped_data/FinalDataScraped.csv')
match_info_df = pd.read_csv('/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/mens-march-mania-2022/MDataFiles_Stage1/MNCAATourneyCompactResults.csv')

#filter match_info_df to only have 2008 and up
match_info_df = match_info_df[match_info_df['Season'] >= 2008]

match_info_df = match_info_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Step 2: Create outcome variable to balance the dataset
num_matches = len(match_info_df)
half_matches = num_matches // 2
match_info_df.loc[:half_matches - 1, 'Outcome'] = 0  # Team1 wins
match_info_df.loc[half_matches:, 'Outcome'] = 1  # Team2 wins

# Step 3: Assign Team1 and Team2 based on the Outcome
match_info_df['T1_ID'] = np.where(match_info_df['Outcome'] == 0, match_info_df['WTeamID'], match_info_df['LTeamID'])
match_info_df['T2_ID'] = np.where(match_info_df['Outcome'] == 0, match_info_df['LTeamID'], match_info_df['WTeamID'])

# Drop the WTeamID and LTeamID columns as they are no longer needed
match_info_df.drop(columns=['WTeamID', 'LTeamID'], inplace=True)

# Step 4: Merge team statistics for T1 and T2
match_info_df = pd.merge(match_info_df, team_stats_df, left_on=['Season', 'T1_ID'], right_on=['Year', 'Team_name'], how='left')
columns_to_rename = {col: 'T1_' + col for col in match_info_df if col.startswith('Team')}
match_info_df.rename(columns=columns_to_rename, inplace=True)
match_info_df.drop(columns=['Year'], inplace=True)

match_info_df = pd.merge(match_info_df, team_stats_df, left_on=['Season', 'T2_ID'], right_on=['Year', 'Team_name'], how='left')
columns_to_rename = {col: 'T2_' + col for col in match_info_df if col.startswith('Team')}
match_info_df.rename(columns=columns_to_rename, inplace=True)
match_info_df.drop(columns=['Year'], inplace=True)

match_info_df['T1_Team_CONF'] = match_info_df['T1_Team_CONF'].fillna('Unknown')
match_info_df['T2_Team_CONF']  = match_info_df['T2_Team_CONF'].fillna('Unknown')

for t in {'T1_', 'T2_'}:
    for col in {'Team_FTA', 'Team_FGA', 'Team_TO', 'Team_ThreePA', 'Team_SOR_RK', 'Team_SOS_RK', 'Team_Losses', 'Team_GP', 'Team_QUAL_LOSS'}:
            match_info_df[t + col] = match_info_df[t + col].fillna(match_info_df[t + col].max())
        
    for col in team_stats_df.columns.difference({'Year', 'Team_FTA', 'Team_FGA', 'Team_TO', 'Team_ThreePA', 'Team_SOR_RK', 'Team_SOS_RK', 'Team_Losses', 'Team_GP', 'Team_QUAL_LOSS'}):
        match_info_df[t + col] = match_info_df[t + col].fillna(match_info_df[t + col].min())

#print duplicates with same t1_id and t2_id and season

match_info_df.drop_duplicates(inplace=True)
match_info_df = match_info_df.drop(columns = {'WLoc', 'DayNum', 'LScore', 'WScore', 'NumOT'})

unique_conferences = match_info_df['T1_Team_CONF'].unique()

unique_conferences = np.append(unique_conferences, match_info_df['T2_Team_CONF'].unique())

# Step 2: Create dictionary mapping
conference_map = {conf: idx + 1 for idx, conf in enumerate(unique_conferences)}

match_info_df['T1_Team_CONF'] = match_info_df['T1_Team_CONF'].map(conference_map)
match_info_df['T2_Team_CONF'] = match_info_df['T2_Team_CONF'].map(conference_map)

match_info_df.drop(columns=['T1_Team_name', 'T2_Team_name'], inplace=True)
#write to csv called input data
match_info_df.to_csv('/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/input_data.csv', index=False)
