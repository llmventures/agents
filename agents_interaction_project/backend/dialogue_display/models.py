from django.db import models

# Create your models here.

class ConversationLog(models.Model):
    agents = models.CharField(max_length = 1000000000)
    date = models.DateTimeField()
    title = models.CharField(max_length = 1000)
    topic_id = models.CharField(max_length=1000, primary_key = True)
    topic_text = models.CharField(max_length = 1000000000)
    log_text = models.CharField(max_length=100000000)
    engine = models.CharField(max_length = 100)

class StoredPapers(models.Model):
    doi = models.CharField(max_length = 100, primary_key = True)
    title = models.CharField(max_length = 1000)
    authors = models.CharField(max_length = 1000)
    date= models.DateTimeField()
    date_accessed = models.DateTimeField()



    
