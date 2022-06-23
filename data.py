import pandas as pd

df = pd.read_csv('../Campus Sitemap & Taxonomy Work 2021-2022 - Wordpress Campus Sites.csv')

clean_df = df.iloc[7::]
clean_df = clean_df[['Unnamed: 0','Unnamed: 2','Unnamed: 10']]
clean_df.rename(columns={'Unnamed: 0' : 'Status','Unnamed: 2' : 'URL','Unnamed: 10' : 'Tags'}, inplace=True)
clean_df = clean_df[(clean_df['Status']=='To Do')]
clean_df = clean_df.dropna()

print(clean_df)