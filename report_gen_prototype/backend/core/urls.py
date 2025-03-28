from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'agents', AgentView, 'agent')
router.register(r'papers', PaperView, 'papers')
router.register(r'leads', TeamLeadView, 'teamleads')
router.register(r'reports', ReportView, 'reports')
urlpatterns = [
    path('', include(router.urls)),
    path("register/", userRegistrationAPIView.as_view(), name = "register-user"),
    path("login/", UserLoginAPIView.as_view(), name = "login-user"),
    path("logout/", UserLogoutAPIView.as_view(), name = "logout-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("user/", UserInfoAPIView.as_view(), name="user-info")
]