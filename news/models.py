from django.db import models

# Create your models here.
class Source(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
    ]

    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    headline = models.TextField()
    url = models.URLField(max_length=500, null=True, blank=True)
    published_at = models.DateTimeField(db_index=True)
    country = models.CharField(max_length=100)
    sentiment_score = models.FloatField()
    sentiment_label = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, db_index=True)
    keywords = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.headline[:50]}..."