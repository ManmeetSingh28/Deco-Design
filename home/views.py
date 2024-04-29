from django.contrib import auth, messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User  
from django.urls import path
from . import views
from django.core.mail import send_mail
from django.conf import settings
import requests
import smtplib
from email.mime.text import MIMEText
from django.http import HttpResponse
from email.mime.multipart import MIMEMultipart

access_key = '8cS-o53Aq0FjZEf_beLGuWv4CvNRRPE4RK8JfuGPLrU'
base_url = 'https://api.unsplash.com'

def home(request):
    query = 'Interior Designs'
    per_page = 10
    width = 800  # specify the width you want
    height = 600  # specify the height you want

    response = requests.get(f'{base_url}/search/photos', params={'query': query, 'per_page': per_page}, headers={'Authorization': f'Client-ID {access_key}'})

    if response.status_code == 200:
        data = response.json()
        filtered_photos = []
        for photo in data['results']:
            if photo['width'] >= width and photo['height'] >= height:
                filtered_photos.append(photo)
        
        image_urls = [photo['urls']['regular'] for photo in filtered_photos]
    else:
        print('Error:', response.status_code)
        image_urls = []
    
    context = {'page_name': 'Deco | Design', 'image_urls': image_urls}
    return render(request, "home.html", context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.error(request, 'Invalid Username or Password')
            return redirect('login')
    else:
        # If it's not a POST request, render the login form
        context = {'page_name': 'Login Deco | Design'}
        return render(request, "login.html", context)



def register(request):
    
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')  # Fix: Redirect to 'register' instead of register
            else:
                user = User.objects.create_user(username=username, password=password1, first_name=first_name, last_name=last_name, email=email)
                user.save()
                auth.login(request, user)  # Fix: Authenticate and login the created user
                messages.success(request, 'Account created successfully')
                return redirect('/')
        else:
            messages.info(request, 'Password Not Matching...')
            return redirect('register')
    
    else:
        context = {'page_name': 'Sign In Deco | Design'}
        return render(request, 'register.html', context)


def logout(request):
    auth.logout(request)
    return redirect("/")



def contact(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname', '')
        email = request.POST.get('email', '')
        number = request.POST.get('number', '')  # Uncomment if 'number' is a field
        message = request.POST.get('message', '')

        # Construct email message
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = 'decodesign28603@gmail.com'
        msg['Subject'] = fullname
        msg.attach(MIMEText(message, 'plain'))

        # SMTP authentication
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, 'decodesign28603@gmail.com', msg.as_string())
            server.sendmail('decodesign28603@gmail.com', email, 'Thank You For Contacting With Deco Designs. Our Team Will Respond You shortly')
            server.quit()
            return render(request, 'response.html')
        except Exception as e:
            print("Error:", str(e))
            return HttpResponse("Error sending email")

    else:
        context = {'page_name': 'Contact Deco | Design'}
        return render(request, 'contact.html', context)


def response(request):
    context = {'page_name': 'Response Deco | Design'}
    return render(request, 'response.html', context)


def school(request):
    query = 'School Interior Designs'
    per_page = 20
    width = 800  # specify the width you want
    height = 600  # specify the height you want

    response = requests.get(f'{base_url}/search/photos', params={'query': query, 'per_page': per_page}, headers={'Authorization': f'Client-ID {access_key}'})

    if response.status_code == 200:
        data = response.json()
        filtered_photos = []
        for photo in data['results']:
            if photo['width'] >= width and photo['height'] >= height:
                filtered_photos.append(photo)
        
        image_urls = [photo['urls']['regular'] for photo in filtered_photos]
    else:
        print('Error:', response.status_code)
        image_urls = []
    
    context = {'page_name': 'School Deco | Design', 'image_urls': image_urls}
    return render(request, "school.html", context)