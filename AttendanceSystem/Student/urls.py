from django.urls import path
from . import views
from .views import StudentLogin

urlpatterns = [

path('Student-Home/', views.home, name='Student-Home'),
path('Student-login/', StudentLogin.as_view(), name="Student_login"),
]