from rest_framework import serializers
from .models import Agent, Report, TeamLead, Paper, CustomUser
from django.contrib.auth import authenticate

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect credentials")
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email')

class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password1', 'password2')
        extra_kwargs = {"password":{"write_only":True}}

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match")
        
        password = attrs.get("password1", "")
        if len(password) < 8:
            raise serializers.ValidationError("Passwords must be at least 8 characters")
        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop("password1")
        validated_data.pop("password2")

        return CustomUser.objects.create_user(password=password, **validated_data)
class PaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paper
        fields = ('file','name', 'id', 'file_type', 'user')
        extra_kwargs = {"user": {"read_only": True}}

class AgentSerializer(serializers.ModelSerializer):
    stored_papers = PaperSerializer(many=True)
    class Meta:
        model = Agent
        fields = ('name','role','expertise','knowledge', 'stored_papers', 'kb_path')



class ReportSerializer(serializers.ModelSerializer):
    lead_name = serializers.CharField(source='lead.name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    context = PaperSerializer(many=True)
    potential_agents = AgentSerializer(many=True)
    chosen_team = AgentSerializer(many=True)
    class Meta:
        model = Report
        fields = ('name','date','task','expectations','context','cycles','report_guidelines','method','temperature','engine', 'model', 'lead_name', 'potential_agents', 'chosen_team', 'output', 'chat_log', 'username', 'saved_to_lead')

class TeamLeadSerializer(serializers.ModelSerializer):
    reports = ReportSerializer(many=True, read_only=True)
    class Meta:
        model = TeamLead
        fields = ('name','description', 'reports','kb_path')
