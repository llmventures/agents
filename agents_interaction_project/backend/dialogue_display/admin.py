from django.contrib import admin
from .models import ConversationLog, StoredPapers
class ConversationLogAdmin(admin.ModelAdmin):
    list_display = ('agents', 'title','date','topic_id','topic_text','log_text','engine')

class StoredPapersAdmin(admin.ModelAdmin):
    list_display = ('doi','title','authors','date', 'date_accessed')

# Register your models here.


admin.site.register(ConversationLog, ConversationLogAdmin)

admin.site.register(StoredPapers, StoredPapersAdmin)