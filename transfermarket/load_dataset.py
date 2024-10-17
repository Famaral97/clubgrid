import pandas as pd

# Load the CSV files into DataFrames
my_data = pd.read_csv('ClubGrid Logo Labelling - ALL_DATA.csv')
other_data = pd.read_csv('clubs.csv')

# Perform an inner merge on the 'club_id' column
merged_data = pd.merge(my_data, other_data, left_on='Tfmk ID', right_on='club_id', how='inner')

# Save the merged data to a new CSV file
merged_data.to_csv('../data/data.csv', index=False, encoding='utf-8')

print("Data merged successfully and saved to /data/data.csv")
