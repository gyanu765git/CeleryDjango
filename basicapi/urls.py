
from django.urls import path
from .views import *

urlpatterns = [
    path('basicapi/', ExecuteTask.as_view(), name = "abc")
]
