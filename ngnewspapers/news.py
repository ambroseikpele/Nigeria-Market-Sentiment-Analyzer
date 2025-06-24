from . import guardian, punch, thesun
import pandas as pd

def get_news():
    news= pd.concat(
        [guardian.scrape(), punch.scrape(), thesun.scrape()],
    )

    # Sort by date so that null dates come last
    news = news.sort_values(by='date', na_position='last')

    # Drop duplicates based on headline, keeping the first occurrence
    news = news.drop_duplicates(subset='headline', keep='first')

    # Reset the index
    news = news.reset_index(drop=True)

    return news
