from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image


# obj = course.objects.all()
# CHOICES = [tuple([e.id, e.id]) for e in obj]

CHOICES = (
    ('Male', ("Male")),
    ('Female', ("Female"))
)

class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    rollno = models.IntegerField(default=0)
    gender = models.CharField(max_length=6,choices= CHOICES , default="Male")
    # subject = models.CharField(max_length=100, choices=CHOICES, default='NONE')
    # subject = models.ForeignKey(course, on_delete=models.CASCADE,)
    
class course(models.Model):
    c_name = models.CharField(max_length=100)
    c_hr = models.IntegerField()
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    registration = models.ManyToManyField(CustomUser, related_name='registration', through='registration')
    attendance = models.ManyToManyField(CustomUser, through='attendance', related_name='attendance')

    def __str__(self):
        return self.c_name


class registration(models.Model):
    # status = models.CharField(max_length=1)
    course = models.ForeignKey(course, on_delete=models.CASCADE, related_name='registration_course')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='registration_student')

    # date = models.DateField()
    class Meta:
        unique_together = [["course", "student"]]


class attendance(models.Model):
    status = models.CharField(max_length=1)
    course = models.ForeignKey(course, on_delete=models.CASCADE, related_name='attendance_course')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='attendance_student')
    date = models.DateField()

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
