from .models import Source, Article
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from collections import Counter
from dotenv import load_dotenv
import nltk
import requests
import os
import logging

logger = logging.getLogger(__name__)

load_dotenv()

try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords', quiet=True)
    stop_words = set(stopwords.words('english'))

analyzer = SentimentIntensityAnalyzer()

NEWS_API_KEY = os.getenv('NEWS_API_KEY')
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

def extract_keywords(text):
    if not text:
        return ""
    words = [w.lower() for w in text.split() if w.isalpha() and w.lower() not in stop_words]
    return ', '.join([w for w, _ in Counter(words).most_common(5)])

def fetch_and_store_articles(country='us'):
    params = {
        'apiKey': NEWS_API_KEY,
        'country': country,
        'pageSize': 100
    }
    
    try:
        response = requests.get(NEWS_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch news from API: {e}")
        return

    if data.get('status') == 'error':
        logger.error(f"NewsAPI error: {data.get('code')} - {data.get('message')}")
        return

    articles_data = data.get('articles', [])
    logger.info(f"Successfully fetched {len(articles_data)} articles.")
    
    for item in articles_data:
        article_url = item.get('url')
        headline = item.get('title')
        
        # Skip if essential data is missing
        if not article_url or not headline:
            continue
            
        source_obj, _ = Source.objects.get_or_create(
            name=item['source']['name'],
            defaults={'country': country}
        )

        sentiment_dict = analyzer.polarity_scores(headline)
        sentiment_score = sentiment_dict['compound']
        if sentiment_score >= 0.05:
            label = 'positive'
        elif sentiment_score <= -0.05:
            label = 'negative'
        else:
            label = 'neutral'

        keywords = extract_keywords(headline)

        Article.objects.update_or_create(
            url=article_url,
            defaults={
                'headline': headline,
                'source': source_obj,
                'published_at': datetime.fromisoformat(item['publishedAt'].replace("Z", "+00:00")),
                'country': country,
                'sentiment_score': sentiment_score,
                'sentiment_label': label,
                'keywords': keywords
            }
        )

