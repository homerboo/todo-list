from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

def index(request):
    return render(request, 'todo/index.html')

def signupUser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
    else:
        username = request.POST['username']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']

        if pass1 == pass2:
            # try except is for duplicate user check
            try:
                # Create a user object
                user = User.objects.create_user(
                    username=usernmame,
                    password=pass1)
                # Save the user object
                user.save()
                # Log the user in
                login(request, user)
                # Send the user to their current to do list
                return redirect('currentToDos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'User already is exist'})

            return render(request, 'todo/signupuser.html')
        else:
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords diddn match'})

def loginUser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('currentToDos')
        else:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':'You shall not pass!'})
        


def logoutUser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')


def currentToDos(request):
    return render(request, 'todo/currenttodos.html')