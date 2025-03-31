from django.urls import path, re_path
from .views import forward_request

urlpatterns = [
    re_path(r'^(?P<path>.*)$', forward_request),  # Catch-all pattern
]
