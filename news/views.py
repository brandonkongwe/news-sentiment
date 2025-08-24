from django.shortcuts import render
from .models import Article, Source
from django.db.models import Avg
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator

def dashboard(request):
    last_week = timezone.now() - timedelta(days=7)
    articles = Article.objects.filter(published_at__gte=last_week)

    source_filter = request.GET.get('source')
    sentiment_filter = request.GET.get('sentiment')
    if source_filter and source_filter != 'all':
        articles = articles.filter(source__id=source_filter)
    if sentiment_filter and sentiment_filter != 'all':
        articles = articles.filter(sentiment_label=sentiment_filter)

    avg_sentiments = articles.order_by('published_at').values('published_at').annotate(avg_sentiment=Avg('sentiment_score'))
    dates = [a['published_at'].strftime("%d-%m-%Y %H:%M") for a in avg_sentiments]
    avg_vals = [a['avg_sentiment'] for a in avg_sentiments]

    paginator = Paginator(articles.order_by('-published_at'), 10) 
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    sources = Source.objects.all()
    return render(request, 'news/dashboard.html', {
        'dates': dates,
        'avg_sentiments': avg_vals,
        'articles': page_obj, 
        'sources': sources,
        'selected_source': source_filter or 'all',
        'selected_sentiment': sentiment_filter or 'all',
    })