from django.db import models
import os

# Create your models here.

class Paper(models.Model):#Note for paper
    #paper should be many to many: as in, not only can a report/agent have
    #many papers, a paper can be associated with multipel agents/reports
    #Site includes display of all prev papers to choose from, as well
    #as opt to upload new
    name = models.CharField(max_length = 100)
    file = models.FileField(upload_to='papers/', null=True, blank=True)
    def filename(self):
        return os.path.basename(self.file.name)

#On agent creation: knowledge base PATH stored. 
#Q: do you want the knowledge base folder+instantiate knowledgebaseobj at agent creation YES
class Agent(models.Model):
    name = models.CharField(max_length = 50)
    role = models.CharField(max_length = 100)
    expertise = models.CharField(max_length = 100)
    knowledge = models.CharField(max_length = 150)#path to knowledge base obj folder
    stored_papers = models.ManyToManyField(Paper, related_name='agents')

class TeamLead(models.Model):
    name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 100)
    
class Report(models.Model):
    name = models.CharField(max_length = 50)
    date = models.DateTimeField()
    task= models.CharField(max_length = 1000)
    expectations=models.CharField(max_length = 1000)
    context=models.ManyToManyField(Paper, related_name='reports')
    cycles=models.IntegerField()
    report_guidelines=models.CharField(max_length = 1000)
    method=models.IntegerField(),
    temperature=models.FloatField(),
    engine = models.CharField(max_length = 50),
    lead = models.ForeignKey(TeamLead, on_delete=models.SET_NULL, null=True,related_name='reports') 

