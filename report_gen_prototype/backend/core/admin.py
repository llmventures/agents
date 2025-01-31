from django.contrib import admin
from .models import Agent, Report, TeamLead, Paper
# Register your models here.

class AgentAdmin(admin.ModelAdmin):
    list_display = ('name','role','expertise','knowledge','get_stored_papers')
    def get_stored_papers(self, obj):
        return "\n".join([str(stored_papers) for stored_papers in obj.knowledge.all()])
class ReportAdmin(admin.ModelAdmin):
    def get_context(self, obj):
        return "\n".join([str(context) for context in obj.context.all()])
    list_display =  ('name','date','task','expectations','get_context','cycles','report_guidelines','method','temperature','engine', 'lead')
class TeamLeadAdmin(admin.ModelAdmin):
    list_display = ('name','description')

class PaperAdmin(admin.ModelAdmin):
    list_display = ('file','name')


admin.site.register(Agent, AgentAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(TeamLead, TeamLeadAdmin)
admin.site.register(Paper, PaperAdmin)

