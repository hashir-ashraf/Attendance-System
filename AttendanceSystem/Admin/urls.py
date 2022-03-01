from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import AdminLogin


urlpatterns = [
    path('', views.frontPage),

    path('front_page', views.frontPage, name='front-page'),
path('Admin-login/', AdminLogin.as_view(), name="Admin_login"),
    path('Admin-logout/', auth_views.LogoutView.as_view(template_name='Admin/logout.html'), name='Admin_logout'),
    path('Admin-password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='Admin/password_reset.html'
         ),
         name='Admin_password_reset'),
    path('Admin-password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='Admin/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('Admin-password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='Admin/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('Admin-password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='Admin/password_reset_complete.html'
         ),
         name='password_reset_complete'),




    path('Admin-Home/', views.home, name='Admin-Home'),
    path('Admin-check/<int:id>', views.check, name='Admin-check'),
    path('Admin-Profile/', views.profile, name='Admin_profile'),

    path('Admin-Student-operations/', views.studentoperations, name='Student_operations'),
    path("Admin-Student-operations/<int:id>", views.deletestudent, name='delete_student'),
    path('Admin-Add-Student/', views.addStudent, name='add-Student'),
    path('Admin-update-student-Profile/<int:iid>', views.student_profile_update_by_admin,
         name='Admin_update_student_profile'),

    path('Admin-update-instructor-Profile/<int:iid>', views.instructor_profile_update_by_admin,
         name='Admin_update_instructor_profile'),
    path('Admin-Instructor-operations/', views.instructoroperations, name='Instructor_operations'),
    path("Admin-Instructor-operations/<int:id>", views.deleteInstructor, name='delete_instructor'),
    path('Admin-Add-Instructor/', views.addInstructor, name='add-Instructor'),

    path('Admin-Course-operations/', views.courseoperations, name='Course-Operations'),
    path("Admin-Course-operations/<int:id>", views.deletecourse, name='delete_course'),

    path('Admin-Add-Course/', views.addCourse, name='add-Course'),


]