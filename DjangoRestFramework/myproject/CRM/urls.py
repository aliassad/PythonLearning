from django.urls import path
from . import views


urlpatterns = [
    path('', views.EmployeeList.as_view())
]
