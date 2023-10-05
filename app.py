import pandas as pd
import streamlit as st
import plotly.express as px
from time import sleep

import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import main
import sentimentOverTime

st.title("Nigeria Market Sentiment Analysis")

while True:
    df= main.get_sentiment()
    
    ### create pie chart
    pie= df[['headline', 'sentiment']].groupby(['sentiment'], as_index=False).count().sort_values(['sentiment'])
    # Create the pie chart using Plotly
    colors = ['gray', 'green', 'red']
    fig = px.pie(values=pie['headline'], names=pie['sentiment'], color_discrete_sequence=colors)
    # Customize the layout
    fig.update_layout(
        title='Sentiment Pie Chart',
        font=dict(size=18),  # Increase font size
        legend_font=dict(size=18)  # Increase legend font size
    )
    
    
    # Display the pie chart in Streamlit
    st.plotly_chart(fig)
    
    
    ### create line chart 
    sentiment_over_time= sentimentOverTime.get_df(df)
    
    # sentiment_tracker = ...
    
    # Define custom colors for sentiments
    color_map = {
        'positive': 'green',
        'neutral': 'gray',
        'negative': 'red'
    }
    
    # Create the line plot with custom colors
    fig = px.line(sentiment_over_time, x='date', y='percentage', color='sentiment', 
                  title='Sentiment Analysis Over Time', 
                  color_discrete_map=color_map)
    
    # Show the plot
    st.plotly_chart(fig)
    
    
    # Combine all headlines into a single string
    text = ' '.join(df['headline'])
    
    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='black', stopwords=STOPWORDS).generate(text)
    
    # Display the word cloud in Streamlit
    st.write("Word Cloud")
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
    sleep(3600)
st.write('Hello, *World!* :sunglasses:')
