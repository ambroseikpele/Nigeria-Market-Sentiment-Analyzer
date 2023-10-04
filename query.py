import pandas as pd

df= pd.read_csv('news.csv')

naira = ['naira', 'ngn', 'fx', 'foreign exchange']
stock=['stock', 'ngx', 'investors']

print(df.dtypes)
# Use a lambda function to check if any word in the list appears in the 'text' column
filtered_df = df[df['headline'].str.lower().apply(lambda x: any(word in x for word in naira))]
print(filtered_df)
