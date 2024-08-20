from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.
class Agent(models.Model):
    name = models.CharField(max_length=30)
    role = models.CharField(max_length=1000)
    agent_type = models.CharField(max_length=30)
    goal = models.CharField(max_length=1000)
    backstory = models.CharField(max_length=1000)
    

class ContextBin(models.Model):
    name = models.CharField(max_length=30)
    links = models.CharField(max_length = 500)
    text = models.CharField(max_length = 700000)



class Task(models.Model):
    name = models.CharField(max_length=30)
    task_time = models.PositiveIntegerField()
    description = models.CharField(max_length=500)
    input_format = models.CharField(max_length=30)
    output_format = models.CharField(max_length=30)

class Edge(models.Model):
    source_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, related_name='source')
    source_object_id = models.PositiveIntegerField()
    source = GenericForeignKey('source_content_type', 'source_object_id')

    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, related_name='target')
    target_object_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_content_type', 'target_object_id')
    
    relation_type = models.CharField(max_length=30)

class Crew(models.Model):
    name = models.CharField(max_length=30,primary_key = True)
    agents = models.JSONField()
    task = models.CharField(max_length=30)
    input_format = models.CharField(max_length=30)
    output_format = models.CharField(max_length=30)

