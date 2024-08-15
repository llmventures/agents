from django.contrib import admin
from .models import Agent, Crew


class AgentAdmin(admin.ModelAdmin):
    list_display = ('name','role','goal','backstory','input_format','output_format')

class CrewAdmin(admin.ModelAdmin):
    list_display = ('name','agents','task','input_format','output_format')



# Register your models here.


admin.site.register(Agent, AgentAdmin)
admin.site.register(Crew, CrewAdmin)
#admin.site.register(Edge, EdgeAdmin)

