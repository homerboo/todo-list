from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import ToDoForm
from .models import Todo
from django.utils import timezone

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
    todos = Todo.objects.all().order_by('-created').filter(fk_user=request.user.id, datecompleted__isnull=True)
    context = {'todos': todos}
    return render(request, 'todo/currenttodos.html', context)

def createToDo(request):
    # a GET means wants the form to make a to do
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form':ToDoForm()})

    # a POST means user wants CRUD with a to do
    else:
        try:
            # parses form submission details
            form = ToDoForm(request.POST)
            # creates a staged version because of False
            submittedToDo = form.save(commit=False)
            # append user to object, save, and show todos
            submittedToDo.fk_user = request.user
            submittedToDo.save()
            return redirect('currentToDos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': ToDoForm(), 'error': 'Bad data passed in'})

def viewToDo(request, todo_pk):
    # third parameter ensures that users cannot bypass the URL and get someone else's todo 
    todo = get_object_or_404(Todo, pk=todo_pk, fk_user=request.user)
    if request.method == 'GET':
        form = ToDoForm(instance=todo)
        context = {'detail': todo, 'form':form}
        return render(request, 'todo/detail.html', context)
    else:
        try:
            form = ToDoForm(request.POST, instance=todo)
            form.save()
            return redirect('viewToDo',todo_pk=todo_pk)
        except ValueError:
            return render(request, 'todo/detail.html', {'todo':todo,'form':form, 'error':'Bad data passed in'})

def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, fk_user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currentToDos')

# def completeToDo(request, todo_pk):
#     todo = get_object_or_404(Todo, pk=todo_pk, fk_user=request.user)
#     if request.method == 'POST':
#         # update the datecompleted to now
#         todo.datecompleted = timezone.now()
#         # save
#         todo.save()
#         # back to current list
#         return redirect('currentToDos')