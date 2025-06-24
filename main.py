import pandas as pd
from ngnewspapers import news
import torch

news_df = news.get_news()
news_df['date'] = pd.to_datetime(news_df['date'], format='%d/%m/%Y')

# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text-classification", model="ProsusAI/finbert")

# Load model directly
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

# Tokenize the headlines
inputs = tokenizer(list(news_df['headline']), return_tensors="pt", padding=True, truncation=True, max_length=512)

# Get model predictions
with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
    probabilities = torch.nn.functional.softmax(logits, dim=-1)
    predicted_indices = torch.argmax(logits, dim=-1)

def get_sentiment():
  global news_df
  # Extract sentiment labels and their corresponding probabilities
  sentiments = [model.config.id2label[idx.item()] for idx in predicted_indices]
  probabilities_list = [prob[predicted_indices[i].item()].item() for i, prob in enumerate(probabilities)]

  # Add the results to the dataframe
  news_df['sentiment'] = sentiments
  news_df['probability'] = probabilities_list
  # Sort by date
  news_df = news_df.sort_values('date')
  news_df.to_csv('news_df.csv', index=False)
  return news_df
