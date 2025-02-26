from django.urls import path
from .views import CampusConnectListCreate, CampusConnectRetrieveUpdateDestroy

urlpatterns = [
    path('v1/campusconnect/', CampusConnectListCreate.as_view(), name='campusconnect-list-create'),
    path('v1/campusconnect/<int:pk>/', CampusConnectRetrieveUpdateDestroy.as_view(), name='campusconnect-retrieve-update-destroy'),
]
