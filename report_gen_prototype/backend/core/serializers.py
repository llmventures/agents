from rest_framework import serializers
from .models import Agent, Report, TeamLead, Paper

class PaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paper
        fields = ('file','name', 'id', 'file_type')

class AgentSerializer(serializers.ModelSerializer):
    stored_papers = PaperSerializer(many=True)
    class Meta:
        model = Agent
        fields = ('name','role','expertise','knowledge', 'stored_papers', 'kb_path')



class ReportSerializer(serializers.ModelSerializer):
    lead_name = serializers.CharField(source='lead.name', read_only=True)
    context = PaperSerializer(many=True)
    potential_agents = AgentSerializer(many=True)
    chosen_team = AgentSerializer(many=True)
    class Meta:
        model = Report
        fields = ('name','date','task','expectations','context','cycles','report_guidelines','method','temperature','engine', 'model', 'lead_name', 'potential_agents', 'chosen_team', 'output', 'chat_log')

class TeamLeadSerializer(serializers.ModelSerializer):
    reports = ReportSerializer(many=True, read_only=True)
    class Meta:
        model = TeamLead
        fields = ('name','description', 'reports','kb_path')
