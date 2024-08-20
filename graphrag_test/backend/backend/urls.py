from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from chatbot import views

router = routers.DefaultRouter()
router.register(r'agents', views.AgentView, 'agent')
router.register(r'crews', views.CrewView, 'crew')
router.register(r'edges', views.EdgeView, 'edge')
router.register(r'context', views.ContextBinView, 'contextbin')
router.register(r'task', views.TaskView, 'task')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/run-crew/', views.run_Crew, name='run-crew'),
    path('api/crew-graphes/', views.save_crewgraph, name = 'crew-graphes')
]