from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from dialogue_display import views

router = routers.DefaultRouter()
router.register(r'conversation_logs', views.ConversationLogView, 'ConversationLog')
router.register(r'stored_papers', views.StoredPapersView, 'StoredPapers')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

    path('api/get-all-papers/', views.getStoredPapers, name = 'get-all-papers'),
    path('api/papers/<str:doi>/', views.getPaperFromDOI, name= 'get-paper-from-doi'),
    path('api/get-all-logs/', views.getAllConvoLogs, name = 'get-all-convo-logs'),
    path('api/get-latest-convo-log/', views.getMostRecentConvoLog, name = 'get-latest-convo-log'),
    path('api/add-convo-log/', views.addConvoLog, name='add-convo-log'),
    path('api/add-stored-paper/', views.addStoredPaper, name='add-stored-paper'),
    path('api/convo-logs/<str:date>/', views.getSpecificLogFromDate, name='get-log-from-date')
]