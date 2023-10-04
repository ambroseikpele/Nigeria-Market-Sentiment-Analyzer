import pandas as pd


def get_df(df):
  # Calculate the count of each sentiment for each date
  sentiment_count = df.groupby(['date', 'sentiment']).size().reset_index(name='count')

  # Calculate the total count of headlines for each date
  total_count = df.groupby('date').size().reset_index(name='total_count')

  # Merge the two dataframes to get total_count alongside each sentiment count
  merged = sentiment_count.merge(total_count, on='date')

  # Calculate the percentage
  merged['percentage'] = (merged['count'] / merged['total_count']) * 100

  # Sort by date
  df = merged.sort_values('date')

  # List of unique dates and sentiments
  unique_dates = df['date'].unique()
  sentiments = ['negative', 'neutral', 'positive']

  # Iterate over each unique date
  for date in unique_dates:
      # Filter dataframe for the current date
      df_date = df[df['date'] == date]
      
      # Check for missing sentiments
      for sentiment in sentiments:
          if sentiment not in df_date['sentiment'].values:
              # If sentiment is missing, append a new row with 0 values
              total = df_date['total_count'].iloc[0]  # Assuming total is the same for a given date
              df = df.append({'date': date, 'sentiment': sentiment, 'count': 0, 'total_count': total, 'percentage': 0}, ignore_index=True)

  # Sort dataframe by Date and Sentiment for better visualization
  df = df.sort_values(by=['date', 'sentiment']).reset_index(drop=True)


  return df