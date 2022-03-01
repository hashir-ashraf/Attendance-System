from django.shortcuts import render, redirect
from django.apps import apps
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.contrib.auth import login




class StudentLogin(LoginView):

    template_name = 'Student/login.html'

    def post(self, request):
        username = request.POST['username']
        User = get_user_model()
        user = User.objects.get(username=username)

        if user.is_student == 1:
            login(request, user)

            return redirect('Student-Home')
        else:
            return render(request, 'Admin/FrontPage.html')


def home(request):
    course = apps.get_model('Admin', 'course')
    registration = apps.get_model('Admin', 'registration')
    attendance = apps.get_model('Admin', 'attendance')
    courses = request.user.registration.all()
    data = {'courses': courses}

    if request.method == 'POST':
        a = int(request.POST.get('course'))
        c = course.objects.get(id=a)
        a = attendance.objects.filter(course=c, student=request.user)
        data['attendence'] = a
        print(data)
        return render(request, 'Student/home.html', data)
    else:
        return render(request, 'Student/home.html', data)
