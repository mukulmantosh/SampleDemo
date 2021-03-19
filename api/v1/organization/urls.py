from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrganizationAPI.as_view()),
    path('<int:pk>', views.OrganizationRetrieveUpdateDestroyAPI.as_view()),
]