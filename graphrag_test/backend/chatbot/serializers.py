from rest_framework import serializers
from .models import Agent, Crew, Edge, ContextBin, Task

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ('agent_type','name','role','goal','backstory')

class ContextBinSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContextBin
        fields = ('name','links')



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('name','description','task_time','input_format','output_format')

class EdgeSourceTargetRelatedField(serializers.RelatedField):
    print("SDJFISDFJOFDJIFSDJOIFJ")
    def to_representation(self, value):
        if isinstance(value, ContextBin):
            serializer = ContextBinSerializer(value)
            
            print(serializer.data)
            return serializer.data
        elif isinstance(value, Agent):
            serializer = AgentSerializer(value)
            return serializer.data 
        
        elif isinstance(value, Task):
            serializer = TaskSerializer(value)
            return serializer.data
        return None
        


class EdgeSerializer(serializers.ModelSerializer):
    source = EdgeSourceTargetRelatedField(read_only=True)
    target = EdgeSourceTargetRelatedField(read_only=True)
    
    class Meta:
        model = Edge
        fields = ('source','target','relation_type')




class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ('name','agents','task','input_format','output_format')