from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('api/<str:entity>/', views.get_entities, name='get_entities'),
    path('api/<str:entity>/<int:id>/', views.get_entity, name='get_entity'),
    path('api/schema/', views.get_schema, name='get_schema'),
    path('api/regenerate/', views.regenerate_data, name='regenerate_data'),
    path('', include(router.urls)),
]