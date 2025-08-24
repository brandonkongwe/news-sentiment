from celery import shared_task
from .services import fetch_and_store_articles

@shared_task
def fetch_news_task():
    fetch_and_store_articles()