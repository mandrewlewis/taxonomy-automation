import pandas as pd

df = pd.read_csv('Campus Sitemap & Taxonomy Work 2021-2022 - Wordpress HS Sites.csv')

clean_df = df.iloc[7::]
clean_df = clean_df[['SPECIAL INSTRUCTIONS','Unnamed: 2','Unnamed: 10','Unnamed: 16']]
clean_df.rename(columns={'SPECIAL INSTRUCTIONS' : 'Status','Unnamed: 2' : 'URL','Unnamed: 10' : 'Tags'}, inplace=True)
# clean_df = clean_df[(clean_df['Status']=='To Do')]
clean_df = clean_df.dropna()
print(clean_df)



# print()
# for i in range(len(clean_df)):
#     print(f'GSuite row: {clean_df.iloc[i].name}')

#     tagSets = []
#     for tagSet in clean_df.iloc[i].Tags.split(','):
#         tagSets.append(tagSet.strip())

#     for tagSet in tagSets:
#         tags = tagSet.split('/')
#         print(tags)

#     print()

# print(f'Length = {len(clean_df)}')
# print()