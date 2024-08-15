from django.db import models

# Create your models here.
class Agent(models.Model):
    name = models.CharField(max_length=30, primary_key = True)
    role = models.CharField(max_length=30)
    goal = models.CharField(max_length=100)
    backstory = models.CharField(max_length=100)
    input_format = models.CharField(max_length=30)
    output_format = models.CharField(max_length=30)

class Edge(models.Model):
    source = models.ForeignKey(Agent, related_name = "outgoing_edges", on_delete=models.CASCADE)
    target = models.ForeignKey(Agent, related_name = "incoming_edges", on_delete=models.CASCADE,null=True, blank=True)

class Crew(models.Model):
    name = models.CharField(max_length=30,primary_key = True)
    agents = models.JSONField()
    task = models.CharField(max_length=30)
    input_format = models.CharField(max_length=30)
    output_format = models.CharField(max_length=30)

