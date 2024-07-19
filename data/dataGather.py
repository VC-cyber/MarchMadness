import pandas as pd
import difflib

# Load MTeams.csv to get team IDs
mteams_df = pd.read_csv('/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/mens-march-mania-2022/MDataFiles_Stage1/MTeams.csv')

# Create a dictionary to map full team names to IDs
team_name_to_id = pd.Series(mteams_df.TeamID.values, index=mteams_df.TeamName).to_dict()
dict_keys = {"Ole Miss Rebels": "Mississippi", "UConn Huskies": "Connecticut", "UT Rio Grande Valley Vaqueros": "UTRGV", "East Tennessee State Buccaneers": "ETSU", "Western Kentucky Hilltoppers": "WKU"
, "Queens University Royals": "Charlotte"}
failures = {}

def get_user_confirmation(team_name, possible_match):
    response = input(f"Do you want to replace '{team_name}' with '{possible_match}'? (yes/no): ")
    return response.lower() in ['yes', 'y']


# Function to replace team names with IDs using only the first word of the team name in the other files
def replace_team_name_with_id(file_path, output_prefix, dict_keys, failures):
    # Load the CSV file
    df = pd.read_csv(file_path)
    df = df[~df['Team_name'].isin(['Middle Tennessee Blue Raiders', 'North Dakota State Bison', 'South Dakota State Jackrabbits'])]
    updated_team_names = []
    for name in df['Team_name']:
        first_word = name.split()[0]
        if first_word in team_name_to_id and len(name.split()) == 2:
            updated_team_names.append(team_name_to_id[first_word])
        elif name in dict_keys:
            updated_team_names.append(team_name_to_id[dict_keys[name]])
        elif first_word in team_name_to_id and (name not in failures or (name in failures and first_word not in failures[name])):
            if(get_user_confirmation(name, first_word)):
                dict_keys[name] = first_word
                updated_team_names.append(team_name_to_id[first_word])
            else:
                similar_names = difflib.get_close_matches(name, team_name_to_id.keys(), n=6, cutoff=0.3)
                similar_names = [match for match in similar_names if name not in failures or match not in failures[name]]
                if similar_names:
                    possible_match = similar_names[0]
                    if get_user_confirmation(name, possible_match):
                        dict_keys[name] = possible_match
                        updated_team_names.append(team_name_to_id[possible_match])
                    else:
                        updated_team_names.append(name)
                        if(name not in failures):
                            failures[name] = [possible_match]
                        else:
                            failures[name].append(possible_match)
                else:
                    updated_team_names.append(name)
        else:
            # Check for similar names
            similar_names = difflib.get_close_matches(name, team_name_to_id.keys(), n=6, cutoff=0.3)
            similar_names = [match for match in similar_names if name not in failures or match not in failures[name]]
            if similar_names:
                possible_match = similar_names[0]
                if get_user_confirmation(name, possible_match):
                    dict_keys[name] = possible_match
                    updated_team_names.append(team_name_to_id[possible_match])
                else:
                    updated_team_names.append(name)
                    if(name not in failures):
                        failures[name] = [possible_match]
                    else:
                        failures[name].append(possible_match)
            else:
                updated_team_names.append(name)
            
    
    # Replace team names with the confirmed IDs
    df['Team_name'] = updated_team_names
    
    # Save the updated DataFrame to a new CSV file
    updated_file_path = f'/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/scraped_data/{output_prefix}_updated.csv'
    df.to_csv(updated_file_path, index=False)
    print("finished 1")
    return updated_file_path, df

# Function to split DataFrame into chunks of 50 and save each chunk as a new CSV file
def split_into_chunks(df, output_prefix):
    chunk_size = 50
    for i in range(0, len(df), chunk_size):
        chunk_df = df.iloc[i:i+chunk_size]
        chunk_df['Year'] = int(2024-i/50)
        #drop any rows with missing values
        chunk_df.dropna(inplace=True)
        chunk_file_path = f'/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/scraped_data/Chunks/{output_prefix}_chunk_{i//chunk_size + 1}.csv'
        chunk_df.to_csv(chunk_file_path, index=False)
        print(f'Saved chunk {i//chunk_size + 1} to {chunk_file_path}')

    
# File paths and output prefixes

# file_info = [
#    #('/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/scraped_data/old_stuff/BPI_stats.csv', 'BPI_stats'),
#     ('/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/scraped_data/old_stuff/finalStatScrape.csv', 'finalStatScrape'),
#     ('/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/scraped_data/old_stuff/PI_stats.csv', 'PI_stats')
# ]

# for file_path, output_prefix in file_info:
#     updated_file_path, updated_df = replace_team_name_with_id(file_path, output_prefix, dict_keys, failures)

updated_file_info = {
   ('/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/scraped_data/BPI_stats_updated.csv', 'BPI_stats'),
    ('/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/scraped_data/finalStatScrape_updated.csv', 'finalStatScrape'),
    ('/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/scraped_data/PI_stats_updated.csv', 'PI_stats')
}

for file_path, output_prefix in updated_file_info:
    split_into_chunks(pd.read_csv(file_path), output_prefix)

# # Process each file
# # for file_path, output_prefix in file_info:
# #     updated_file_path, updated_df = replace_team_name_with_id(file_path, output_prefix, dict_keys, failures)
#     #df= pd.read_csv(file_path)
#     #print(df)
# #     split_into_chunks(updated_df, output_prefix)

chunk_file_info = [
    ('/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/scraped_data/Chunks/', 'BPI_stats'),
    ('/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/scraped_data/Chunks/', 'finalStatScrape'),
    ('/Users/venkat/Desktop/UCLA_CS/Summer_projects/MarchMadness/data/scraped_data/Chunks/', 'PI_stats')
]


for file_path, output_prefix in chunk_file_info:
    for i in range(1,18):
        df = pd.read_csv(file_path+f'{output_prefix}_chunk_{i}.csv')
        #print(df[df.duplicated(subset=['Team_name', 'Year'])])
    #print redudant ids and years
    