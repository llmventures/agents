from django.contrib import admin
from .models import Agent, Crew, Edge, ContextBin


class AgentAdmin(admin.ModelAdmin):
    list_display = ('name','role','goal','backstory')

class CrewAdmin(admin.ModelAdmin):
    list_display = ('name','agents','task','input_format','output_format')

class EdgeAdmin(admin.ModelAdmin):
    list_display = ('target', 'source','relation_type')

class ContextBinAdmin(admin.ModelAdmin):
    list_display = ('name', 'links')


# Register your models here.


admin.site.register(Agent, AgentAdmin)
admin.site.register(Crew, CrewAdmin)
admin.site.register(Edge, EdgeAdmin)
admin.site.register(ContextBin, ContextBinAdmin)

