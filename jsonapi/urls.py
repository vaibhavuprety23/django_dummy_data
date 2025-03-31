from django.urls import path
from .views import JSONDataView

urlpatterns = [
    path('json-data/', JSONDataView.as_view(), name='json-data'),
]
