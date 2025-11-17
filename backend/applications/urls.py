from django.urls import path
from .views import index, create_application

urlpatterns = [
    path("", index, name="index"),
    path("apply/", create_application, name="create_application"),
]