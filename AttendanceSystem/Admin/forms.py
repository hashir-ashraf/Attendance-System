from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
CHOICES = (
    ('Male', ("Male")),
    ('Female', ("Female"))
)

class InstructorRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    is_instructor = forms.BooleanField(required=True)
    gender = forms.ChoiceField(choices=CHOICES, widget=forms.Select())

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'gender', 'is_instructor']
#
class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    is_student = forms.BooleanField(required=True)
    rollno = forms.IntegerField()
    gender = forms.ChoiceField(choices=CHOICES, widget=forms.Select())

    # subjects = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset = course.objects.all())

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'is_student','rollno','gender']

def fun():
    users = CustomUser.objects.filter(is_instructor=1)
    cources = course.objects.all()
    for c in cources:
        users = users.exclude(id=c.instructor_id)
    return users

class CourseRegistrationForm(forms.ModelForm):
    c_name = forms.CharField()
    c_hr = forms.CharField()
    instructor = forms.ModelChoiceField(queryset= None)

    def __init__(self, *args, **kwargs):
        super(CourseRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['instructor'].queryset = fun()

    class Meta:
        model = course
        fields = ['c_name', 'c_hr', 'instructor']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    gender = forms.ChoiceField(choices=CHOICES, widget=forms.Select())



    class Meta:
        model = CustomUser
        fields = ['username','password', 'first_name', 'last_name', 'email', 'gender']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
