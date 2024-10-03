from rest_framework import serializers
from .models import ConversationLog, StoredPapers

class ConversationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationLog
        fields = ('agents', 'title','date','topic_id','topic_text','log_text','engine')

class StoredPapersSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoredPapers
        fields = ('doi','title','authors','date', 'date_accessed')

