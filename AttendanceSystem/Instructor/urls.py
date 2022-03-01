from django.urls import path
from . import views
from .views import InstructorLogin

urlpatterns = [

path('Instructor-Home/', views.home, name='Instructor-Home'),
path('Instructor-login/', InstructorLogin.as_view(), name="Instructor_login"),

]