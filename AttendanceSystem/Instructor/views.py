import os
from django.conf import settings
from django.shortcuts import render, redirect
import face_recognition
import numpy as np
import cv2
from os.path import dirname, join
from django.apps import apps
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.contrib.auth import login

class InstructorLogin(LoginView):

    template_name = 'Instructor/login.html'

    def post(self, request):
        username = request.POST['username']
        User = get_user_model()
        user = User.objects.get(username=username)

        if user.is_instructor==1:
            login(request, user)

            return redirect('Instructor-Home')
        else:
            return render(request,'Admin/FrontPage.html')







def findEncondings(images):

    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def home(request):
    c_user = apps.get_model('Admin', 'CustomUser')
    Profile = apps.get_model('Admin', 'Profile')
    course = apps.get_model('Admin', 'course')
    registration = apps.get_model('Admin', 'registration')
    attendance = apps.get_model('Admin', 'attendance')
    instructor = request.user
    inst_course = course.objects.get(instructor=instructor)
    students = inst_course.registration.all()
    # path = 'C:/Users/mg/PycharmProjects/testattendence/AttendanceSystem'
    path = settings.BASE_DIR
    images = []
    classNames = []
    students_present = []
    for student in students:
        s_profile = Profile.objects.get(user=student)
        curImg = cv2.imread(f'{path}/media/{s_profile.image}')
        images.append(curImg)
        classNames.append(student.username)
    print(classNames)

    if request.method == 'POST':
        myfile = request.FILES['document']
        print(myfile.name)
        fs = FileSystemStorage()
        imgname = fs.save(myfile.name, myfile)
        url = fs.url(imgname)
        print(url)
        print(imgname)
        date=request.POST.get('Date')
        print(date)
        encodeListKnown = findEncondings(images)
        print('Encoding complete')
        # encoding end

        faces = []
        prototxtPath = join(dirname(__file__), "deploy.prototxt.txt")
        modelPath = join(dirname(__file__), "res10_300x300_ssd_iter_140000.caffemodel")
        # image path
        # imagePath = 'C:/Users/mg/Desktop/DSC_0227.jpg'
        confidence1 = 0.1
        # construct the argument parse and parse the arguments
        # load our serialized model from disk
        print("[INFO] loading model...")
        net = cv2.dnn.readNetFromCaffe(prototxtPath, modelPath)
        # load the input image and construct an input blob for the image
        # by resizing to a fixed 300x300 pixels and then normalizing it
        image = cv2.imread(f'{path}{url}')
        fs.delete(imgname)
        image = cv2.resize(image, (0, 0), None, 0.25, 0.25)
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
                                     (300, 300), (104.0, 177.0, 123.0))
        # pass the blob through the network and obtain the detections and
        # predictions
        print("[INFO] computing object detections...")
        net.setInput(blob)
        detections = net.forward()
        # loop over the detections
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.7:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                faces.append((startY, endX, endY, startX))
        encodesCurFrame = face_recognition.face_encodings(image, faces)
        print("encode")
        for encodeFace, faceLoc in zip(encodesCurFrame, faces):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex]
                students_present.append(name)
                print(name)
                y1, x2, y2, x1 = faceLoc
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(image, (x1, y2 - 35), (x2, y2), (0, 255, 0))
                cv2.putText(image, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                # markAttendence(name)
            else:
                y1, x2, y2, x1 = faceLoc
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(image, (x1, y2 - 35), (x2, y2), (0, 255, 0))
                cv2.putText(image, "unknown", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

        # show the output image
        # cv2.imshow("Output", image)
        # cv2.waitKey(0)
        print(students_present)
        students_present = set(students_present)
        print(students_present)
        marked = []
        for s in students:
            if s.username in students_present:
                stu = c_user.objects.get(username=s)
                obj = attendance()
                obj.student = stu
                obj.course = inst_course
                obj.status = 'p'
                obj.date = request.POST.get('Date')
                obj.save()
                marked.append(obj)
            else:
                stu = c_user.objects.get(username=s)
                obj = attendance()
                obj.student = stu
                obj.course = inst_course
                obj.status = 'A'
                obj.date = request.POST.get('Date')
                obj.save()
                marked.append(obj)
        data = {"marked": marked}
        print(marked[0].course)
        return render(request, 'Instructor/home.html', data)
    else:
        return render(request, 'Instructor/home.html')








