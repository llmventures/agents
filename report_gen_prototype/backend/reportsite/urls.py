"""
URL configuration for reportsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views
from django.urls import path


router = routers.DefaultRouter()
router.register(r'agents', views.AgentView, 'agent')
router.register(r'papers', views.PaperView, 'papers')
router.register(r'leads', views.TeamLeadView, 'teamleads')
router.register(r'reports', views.ReportView, 'reports')
urlpatterns = [
    path('', include('core.urls')),
    path('token/', jwt_views.TokenObtainPairView.as_view(), 
          name ='token_obtain_pair'),
    path('token/refresh/', 
        jwt_views.TokenRefreshView.as_view(), 
        name ='token_refresh'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/test_report/', views.generate_report, name='generate_report'),
    path('api/save_report_memory/<str:name>', views.save_report_memory, name='save_report_memory'),
    path('api/leads/<str:name>/', views.TeamLeadView.as_view({'get': 'retrieve'}), name='lead-detail'),
    path('api/leads/<str:name>/', views.AgentView.as_view({'get': 'retrieve'}), name='agent-detail'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
