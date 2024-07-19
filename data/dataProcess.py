import pandas as pd
import os

# Function to read and preprocess each chunk file
def preprocess_chunk(file_path):
    df = pd.read_csv(file_path)
    # Fill missing values with the minimum for each column
    df = df.fillna(df.min())
    return df

# Function to ensure columns are correctly typed
def ensure_column_types(df, column_types):
    for column, dtype in column_types.items():
        if column in df.columns:
            df[column] = df[column].astype(dtype)
    return df

# Function to merge data for a single chunk
def merge_data_for_chunk(final_stats_file, BP_stats_file, PI_stats_file, output_file):
    final_stats_df = preprocess_chunk(final_stats_file)
    BP_stats_df = preprocess_chunk(BP_stats_file)
    PI_stats_df = preprocess_chunk(PI_stats_file)

    # Define the expected column types
    column_types = {
        'Team_name': str,
        'Team_W_L': str,
        'Team_CONF': str,
        'Team_SOR_RK': int,
        'Team_SOS_RK': int,
        'Team_QUAL_WINS': str,
        'Year': int
    }

    # Ensure column types are correct
    final_stats_df = ensure_column_types(final_stats_df, column_types)
    BP_stats_df = ensure_column_types(BP_stats_df, column_types)
    PI_stats_df = ensure_column_types(PI_stats_df, column_types)

    # Merge final_stats with BP_stats
    merged_df = final_stats_df.copy()

    # Ensure team_id is consistent type
    final_stats_df['Team_name'] = final_stats_df['Team_name'].astype(str)
    BP_stats_df['Team_name'] = BP_stats_df['Team_name'].astype(str)
    PI_stats_df['Team_name'] = PI_stats_df['Team_name'].astype(str)

    # Merge with BP_stats data
    for index, row in merged_df.iterrows():
        team_id = row['Team_name']
        if team_id in BP_stats_df['Team_name'].values:
            bp_data = BP_stats_df.loc[BP_stats_df['Team_name'] == team_id].iloc[0]
            bp_columns = BP_stats_df.columns.difference(final_stats_df.columns)
            merged_df.loc[index, bp_columns] = bp_data[bp_columns].values

    # Add teams from BP_stats not in final_stats
    bp_teams_not_in_final = BP_stats_df[~BP_stats_df['Team_name'].isin(final_stats_df['Team_name'])]
    merged_df = pd.concat([merged_df, bp_teams_not_in_final], ignore_index=True)

    # Merge with PI_stats data
    for index, row in merged_df.iterrows():
        team_id = row['Team_name']
        if team_id in PI_stats_df['Team_name'].values:
            pi_data = PI_stats_df.loc[PI_stats_df['Team_name'] == team_id].iloc[0]
            pi_columns = PI_stats_df.columns.difference(final_stats_df.columns)
            merged_df.loc[index, pi_columns] = pi_data[pi_columns].values
        else:
            # Fill in missing columns from PI_stats with minimum values
            for col in PI_stats_df.columns.difference(final_stats_df.columns):
                if col == 'Team_CONF':
                    merged_df.loc[index, col] = 'Unknown'

    # Add teams from PI_stats not already merged
    pi_teams_not_merged = PI_stats_df[~PI_stats_df['Team_name'].isin(merged_df['Team_name'])]
    merged_df = pd.concat([merged_df, pi_teams_not_merged], ignore_index=True)

    # Drop duplicate columns (like year and ID)
    merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]

    # Split Team_QUAL_WINS into Team_QUAL_WINS and Team_QUAL_LOSS
    merged_df['Team_QUAL_LOSS'] = merged_df['Team_QUAL_WINS'].str.split('-').str[1].astype('Int64')
    merged_df['Team_QUAL_WINS'] = merged_df['Team_QUAL_WINS'].str.split('-').str[0].astype('Int64')

    # Split Team_W_L into Team_Wins and Team_Losses
    merged_df[['Team_Wins', 'Team_Losses']] = merged_df['Team_W_L'].str.split('-', expand=True).astype('Int64')

    # Drop the Team_W_L column
    merged_df = merged_df.drop('Team_W_L', axis=1)

    merged_df['Team_GP'] = merged_df['Team_GP'].astype('Int64')

    for col in {'Team_FTA', 'Team_FGA', 'Team_TO', 'Team_ThreePA', 'Team_SOR_RK', 'Team_SOS_RK', 'Team_Losses', 'Team_GP', 'Team_QUAL_LOSS'}:
        merged_df[col] = merged_df[col].fillna(merged_df[col].max())
    
    for col in merged_df.columns.difference({'Team_FTA', 'Team_FGA', 'Team_TO', 'Team_ThreePA', 'Team_SOR_RK', 'Team_SOS_RK', 'Team_Losses', 'Team_GP', 'Team_QUAL_LOSS'}):
        merged_df[col] = merged_df[col].fillna(merged_df[col].min())

    # Write merged data to CSV
    merged_df.to_csv(output_file, index=False)

# Example usage for a single chunk
for i in range(1,18):  # Adjust the range to process all chunks
    final_stats_file = f'/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/scraped_data/Chunks/finalStatScrape_chunk_{i}.csv'
    BP_stats_file = f'/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/scraped_data/Chunks/BPI_stats_chunk_{i}.csv'
    PI_stats_file = f'/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/scraped_data/Chunks/PI_stats_chunk_{i}.csv'
    output_file = f'/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/scraped_data/FinalChunks/combined_stats_chunk_{i}.csv'
    merge_data_for_chunk(final_stats_file, BP_stats_file, PI_stats_file, output_file)

file_path = f'/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/scraped_data/FinalDataScraped.csv'


for i in range(1,18):
    df = pd.read_csv(f'/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/scraped_data/FinalChunks/combined_stats_chunk_{i}.csv')
    if i == 1:
        combined_df = df
    else:
        combined_df = pd.concat([combined_df, df], ignore_index=True)

#combined_df = combined_df.drop_duplicates()
# Write combined data to CSV


combined_df.to_csv(file_path, index=False)