import pandas as pd
import numpy as np

team_stats_df = pd.read_csv('/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/scraped_data/FinalDataScraped.csv')
match_info_df = pd.read_csv('/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/mens-march-mania-2022/MDataFiles_Stage2/MSampleSubmissionStage2.csv')

match_info_df[['Season', 'T1_ID', 'T2_ID']] = match_info_df['ID'].str.split('_', expand=True).astype(int)

match_info_df = pd.merge(match_info_df, team_stats_df, left_on=['Season', 'T1_ID'], right_on=['Year', 'Team_name'], how='left')
columns_to_rename = {col: 'T1_' + col for col in match_info_df if col.startswith('Team')}
match_info_df.rename(columns=columns_to_rename, inplace=True)
match_info_df.drop(columns=['Year', 'T1_Team_name'], inplace=True)

match_info_df = pd.merge(match_info_df, team_stats_df, left_on=['Season', 'T2_ID'], right_on=['Year', 'Team_name'], how='left')
columns_to_rename = {col: 'T2_' + col for col in match_info_df if col.startswith('Team')}
match_info_df.rename(columns=columns_to_rename, inplace=True)
match_info_df.drop(columns=['Year', 'T2_Team_name'], inplace=True)

match_info_df['T1_Team_CONF'] = match_info_df['T1_Team_CONF'].fillna('Unknown')
match_info_df['T2_Team_CONF']  = match_info_df['T2_Team_CONF'].fillna('Unknown')

for t in {'T1_', 'T2_'}:
    for col in {'Team_FTA', 'Team_FGA', 'Team_TO', 'Team_ThreePA', 'Team_SOR_RK', 'Team_SOS_RK', 'Team_Losses', 'Team_GP', 'Team_QUAL_LOSS'}:
            match_info_df[t + col] = match_info_df[t + col].fillna(match_info_df[t + col].max())
        
    for col in team_stats_df.columns.difference({'Year', 'Team_name', 'Team_FTA', 'Team_FGA', 'Team_TO', 'Team_ThreePA', 'Team_SOR_RK', 'Team_SOS_RK', 'Team_Losses', 'Team_GP', 'Team_QUAL_LOSS'}):
        match_info_df[t + col] = match_info_df[t + col].fillna(match_info_df[t + col].min())

#print duplicates with same t1_id and t2_id and season

match_info_df.drop_duplicates(inplace=True)

unique_conferences = match_info_df['T1_Team_CONF'].unique()

unique_conferences = np.append(unique_conferences, match_info_df['T2_Team_CONF'].unique())

# Step 2: Create dictionary mapping
conference_map = {conf: idx + 1 for idx, conf in enumerate(unique_conferences)}

match_info_df['T1_Team_CONF'] = match_info_df['T1_Team_CONF'].map(conference_map)
match_info_df['T2_Team_CONF'] = match_info_df['T2_Team_CONF'].map(conference_map)

match_info_df.drop(columns = {'ID', 'Pred'}, inplace=True)
#write to csv called input data
match_info_df.to_csv('/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/eval_data.csv', index=False)
