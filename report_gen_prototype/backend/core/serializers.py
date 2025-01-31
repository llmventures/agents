from rest_framework import serializers
from .models import Agent, Report, TeamLead, Paper

class PaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paper
        fields = ('file','name')

class AgentSerializer(serializers.ModelSerializer):
    stored_papers = PaperSerializer(many=True)
    class Meta:
        model = Agent
        fields = ('name','role','expertise','knowledge', 'stored_papers')



class ReportSerializer(serializers.ModelSerializer):
    context = PaperSerializer(many=True)
    class Meta:
        model = Report
        fields = ('name','date','task','expectations','context','cycles','report_guidelines','method','temperature','engine', 'lead')

class TeamLeadSerializer(serializers.ModelSerializer):
    reports = ReportSerializer(many=True, read_only=True)
    class Meta:
        model = TeamLead
        fields = ('name','description', 'reports')
