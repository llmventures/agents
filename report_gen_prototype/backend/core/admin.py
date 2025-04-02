from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Agent, Report, TeamLead, Paper, CustomUser
from .forms import CustomUserChangeForm, CustomUserCreationForm
# Register your models here.
@admin.register(CustomUser)
class CustomAdminUser(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    model = CustomUser

class AgentAdmin(admin.ModelAdmin):
    list_display = ('name','role','expertise','knowledge')
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

