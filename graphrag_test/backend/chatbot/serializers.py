from rest_framework import serializers
from .models import Agent, Crew, Edge

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ('name','role','goal','backstory','input_format','output_format')

class EdgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edge
        fields = ('source','target')

class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ('name','agents','task','input_format','output_format')