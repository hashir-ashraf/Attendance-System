from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.contrib.auth import  login





class AdminLogin(LoginView):

    template_name = 'Admin/login.html'

    def post(self, request):
        username = request.POST['username']

        User = get_user_model()

        user = User.objects.get(username=username)
        if user.is_admin== 1:
            login(request, user)

            return render(request,'Admin/home.html')
        else:
            return render(request,'Admin/FrontPage.html')



@login_required
def home(request):

    return render(request, 'Admin/home.html')



def check(request,id):
    remaining_courses = course.objects.all()
    registered_courses = []
    reg_ids = []
    rem_ids = []
    c = course.objects.all()

    if request.method == 'POST':
        obj =course.objects.all()
        coursenames = [x.c_name for x in obj]
        reg_courseids = []
        unreg_courseids = []
        for x in coursenames:
            reg_courseids.append(int(request.POST.get(x)))if request.POST.get(x) else print('')
        for x in obj:
            unreg_courseids.append(int(request.POST.get(str(x.id))))if request.POST.get(str(x.id)) else print('')
        print(reg_courseids)
        print(unreg_courseids)
        print("id")
        print(id)
        student = CustomUser.objects.get(id=id)
        if reg_courseids:
            for i in reg_courseids:

                obj = course.objects.get(id=i)
                obj.registration.add(student)
        if unreg_courseids:
            for i in unreg_courseids:

                obj = course.objects.get(id=i)
                reg = registration.objects.get(student=student,course=obj)
                # obj = obj.registration.get(registration_student=student)
                print("//")
                print(reg)
                print("//")
                reg.delete()





        return redirect('Student_operations')
    else:
        for cou in c:
            stu = cou.registration.all()
            for s in stu:
                if s.id == id:
                    registered_courses.append(course.objects.get(id=cou.id))
                    remaining_courses = remaining_courses.exclude(id=cou.id)
                    reg_ids.append(cou.id)
        for i in remaining_courses:
            rem_ids.append(i.id)
        print('rem,reg')
        print(rem_ids, reg_ids)
        data = {"courses": remaining_courses,"s_student": CustomUser.objects.get(id=id),'r_courses':registered_courses}
        return render(request, 'Admin/check.html', data)
    # return render(request, 'Admin/check.html')


def frontPage(request):
    return render(request, 'Admin/FrontPage.html')

@login_required
def instructoroperations(request):
    instr_details = {"instructors": CustomUser.objects.filter(is_instructor= 1)}
    print(instr_details)
    return render(request, 'Admin/Instructor-operations.html', instr_details)
@login_required
def addInstructor(request):
    if request.method == 'POST':
        u_form = InstructorRegistrationForm(request.POST)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your Account has been Updated!')
            return redirect('Instructor_operations')
    else:
        u_form = InstructorRegistrationForm()
    context = {
        'u_form': u_form
    }
    return render(request, 'Admin/AddInstructor.html', context)

@login_required
def deleteInstructor(request, id):
    obj = CustomUser.objects.get(id=id)
    obj.delete()
    instr_details = {"instructors": CustomUser.objects.filter(is_instructor= 1)}
    return render(request, 'Admin/Instructor-operations.html', instr_details)



@login_required
def instructor_profile_update_by_admin(request, iid):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=CustomUser.objects.filter(id=iid).first())
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=Profile.objects.filter(user_id=iid).first())
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Account has been Updated!')
            return redirect('Instructor_operations')
    else:
        u_form = UserUpdateForm(instance=CustomUser.objects.filter(id=iid).first())
        p_form = ProfileUpdateForm(instance=Profile.objects.filter(user_id=iid).first())
    context = {
        'u_form':u_form,
        'p_form':p_form
    }

    return render(request, 'Admin/profile.html', context)

@login_required
def courseoperations(request):
    c_details = {"courses": course.objects.all()}
    return render(request, 'Admin/Course-operations.html',c_details)
@login_required
def addCourse(request):
    if request.method == 'POST':
        C_form = CourseRegistrationForm(request.POST)
        if C_form.is_valid():
            C_form.save()
            messages.success(request, f'Course has been Added!')
            return redirect('Course-Operations')
    else:
        C_form = CourseRegistrationForm()
    context = {
        'u_form': C_form
    }

    return render(request, 'Admin/AddCourse.html', context)
@login_required
def deletecourse(request, id):
    obj = course.objects.get(id=id)
    obj.delete()
    c = course.objects.all()
    c_details = {"courses": c}
    return render(request, 'Admin/Course-operations.html', c_details)


@login_required
def addStudent(request):
    if request.method == 'POST':
        u_form = StudentRegistrationForm(request.POST)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your Account has been Updated!')
            return redirect('Student_operations')
    else:
        u_form = StudentRegistrationForm()
    context = {
        'u_form': u_form
    }
    return render(request, 'Admin/AddStudent.html', context)

@login_required
def studentoperations(request):
    student_details = {"students": CustomUser.objects.filter(is_student= 1)}
    print(student_details)
    return render(request, 'Admin/Student-operations.html', student_details)

@login_required
def deletestudent(request, id):
    obj = CustomUser.objects.get(id=id)
    obj.delete()
    student_details = {"students": CustomUser.objects.filter(is_student= 1)}
    return render(request, 'Admin/Student-operations.html', student_details)

@login_required
def student_profile_update_by_admin(request, iid):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=CustomUser.objects.filter(id=iid).first())
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=Profile.objects.filter(user_id=iid).first())
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Account has been Updated!')
            return redirect('Student_operations')
    else:
        u_form = UserUpdateForm(instance=CustomUser.objects.filter(id=iid).first())
        p_form = ProfileUpdateForm(instance=Profile.objects.filter(user_id=iid).first())
    context = {
        'u_form':u_form,
        'p_form':p_form
    }

    return render(request, 'Admin/profile.html', context)



@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Account has been Updated!')
            return redirect('Admin_profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)


    context = {
        'u_form':u_form,
        'p_form':p_form


    }

    return render(request, 'Admin/profile.html', context)

