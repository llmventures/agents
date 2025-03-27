from django.db import models
import os
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD="email"
    REQUIRED_FIELDS=["username"]

    def __str__(self) -> str:
        return self.email

class Paper(models.Model):#Note for paper
    #paper should be many to many: as in, not only can a report/agent have
    #many papers, a paper can be associated with multipel agents/reports
    #Site includes display of all prev papers to choose from, as well
    #as opt to upload new
    name = models.CharField(max_length = 100)
    file = models.FileField(upload_to='papers/', null=True, blank=True)
    file_type = models.CharField(max_length = 50)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='papers')
    def filename(self):
        return os.path.basename(self.file.name)

#On agent creation: knowledge base PATH stored. 
#Q: do you want the knowledge base folder+instantiate knowledgebaseobj at agent creation YES
class Agent(models.Model):
    kb_path = models.CharField(max_length = 100, unique = True)
    name = models.CharField(max_length = 50,unique=True)
    role = models.CharField(max_length = 100)
    expertise = models.CharField(max_length = 100)
    knowledge = models.CharField(max_length = 150)#path to knowledge base obj folder
    stored_papers = models.ManyToManyField(Paper, related_name='agents')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='agents_user')

class TeamLead(models.Model):
    kb_path = models.CharField(max_length = 100, unique = True)
    name = models.CharField(max_length = 50,unique=True)
    description = models.CharField(max_length = 100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='lead')
    
class Report(models.Model):
    name = models.CharField(max_length = 50,unique=True)
    date = models.DateTimeField()
    task= models.CharField(max_length = 1000)
    expectations=models.CharField(max_length = 1000)
    context=models.ManyToManyField(Paper, related_name='reports')
    cycles=models.IntegerField()
    method = models.IntegerField()
    report_guidelines=models.CharField(max_length = 1000)
    method=models.IntegerField()
    temperature=models.FloatField()
    engine = models.CharField(max_length = 50)
    model = models.CharField(max_length = 50)
    lead = models.ForeignKey(TeamLead, on_delete=models.SET_NULL, null=True,related_name='reports') 
    potential_agents = models.ManyToManyField(Agent, related_name='reports_p_agents')#the list of agents the report engien chose from
    chosen_team = models.ManyToManyField(Agent, related_name='reports_chosen_agents')#The actual agents chosen
    output = models.FileField(upload_to='reports/', null=True, blank=True)
    chat_log = models.FileField(upload_to="report_logs/", null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reports_user')