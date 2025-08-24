from .models import Source, Article
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from collections import Counter
from dotenv import load_dotenv
import nltk
import requests
import os

load_dotenv()

nltk.download('stopwords')

analyzer = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words('english'))

NEWS_API_KEY = os.getenv('NEWS_API_KEY')
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

def extract_keywords(text):
    words = [w.lower() for w in text.split() if w.isalpha() and w.lower() not in stop_words]
    return ', '.join([w for w, _ in Counter(words).most_common(5)])

def fetch_and_store_articles(country='us'):
    params = {
        'apiKey': NEWS_API_KEY,
        'country': country,
        'pageSize': 100
    }
    response = requests.get(NEWS_API_URL, params=params)
    data = response.json()
    
    for item in data.get('articles', []):
        source_obj, _ = Source.objects.get_or_create(
            name=item['source']['name'],
            defaults={'country': country, 'url': item['source'].get('url')}
        )

        sentiment_dict = analyzer.polarity_scores(item['title'])
        sentiment_score = sentiment_dict['compound']
        if sentiment_score >= 0.05:
            label = 'positive'
        elif sentiment_score <= -0.05:
            label = 'negative'
        else:
            label = 'neutral'

        keywords = extract_keywords(item['title'])

        Article.objects.update_or_create(
            headline=item['title'],
            defaults={
                'source': source_obj,
                'published_at': datetime.fromisoformat(item['publishedAt'].replace("Z", "+00:00")),
                'country': country,
                'sentiment_score': sentiment_score,
                'sentiment_label': label,
                'keywords': keywords
            }
        )

