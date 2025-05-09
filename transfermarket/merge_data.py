import pandas as pd

cg_data = pd.read_csv('ClubGrid Logo Labelling - ALL_DATA.csv')

tfmkt_data = pd.concat([
    pd.read_csv('scrapped_data_DE.csv'),
    pd.read_csv('scrapped_data_EN.csv'),
    pd.read_csv('scrapped_data_ES.csv'),
    pd.read_csv('scrapped_data_FR.csv'),
    pd.read_csv('scrapped_data_IT.csv'),
    pd.read_csv('scrapped_data_PT.csv'),
])

merged_data = pd.merge(cg_data, tfmkt_data, left_on='tfmk_id', right_on='tfmk_id', how='inner')

merged_data.to_csv('../data/data.csv', index=False, encoding='utf-8')

print("Data merged successfully and saved ./data/data.csv")
