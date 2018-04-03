import logging
import pyrebase
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import auth

config = {
    "apiKey": "",
    "authDomain": "",
    "databaseURL": "",
    "projectId": "",
    "storageBucket": "",
    "messagingSenderId": ""
}

firebase = pyrebase.initialize_app(config)
authen = firebase.auth()
database = firebase.database()


def index(request):
    return render(request, 'home.html')


def login(request):
    auth.logout(request)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = authen.sign_in_with_email_and_password(email, password)
            if user:
                request.session['iud'] = str(user['idToken'])
            return redirect('home')
        except Exception:
            message = 'invalid credentials'
            messages.warning(request, message)
    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    return render(request, 'accounts/login.html')


def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = authen.create_user_with_email_and_password(email, password)
            if user:
                uid = user['localId']
                data = {'name': name, 'status': '1'}
                database.child('users').child(uid).child('details').set(data)
                return redirect('login')
        except Exception as e:
            messages.warning(request, str(e))
    return render(request, 'accounts/signup.html')
