from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'clients', views.ClientViewSet, basename='client')

urlpatterns = [
    path('user/login/', TokenObtainPairView.as_view(), name='user-login'),
    path('user/logout/', TokenBlacklistView.as_view(), name='user-logout'),
    path('clients/<int:id>/projects/', views.CreateProject.as_view(), name='create-project'),
    path('projects/', views.ListUserProjects.as_view(), name='list-projects'),

] + router.urls
