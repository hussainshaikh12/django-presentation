from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Todo, User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError

def index(request):
    if request.user.is_authenticated:
        todo_list = Todo.objects.order_by('-created_at')
        print(todo_list)
        return render(request, "todos/index.html", {"todo_list": todo_list})

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("todos:login"))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("todos:index"))
        else:
            return render(request, "todos/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "todos/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("todos:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "todos/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username=email, email=email, password=password)
            user.save()
        except IntegrityError:
            return render(request, "todos/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("todos:index"))
    else:
        return render(request, "todos/register.html")

def add(request):
    user = User.objects.get(username=request.user)
    title = request.POST['title']
    Todo.objects.create(user= user,title=title)

    return redirect('todos:index')

def delete(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    todo.delete()

    return redirect('todos:index')

def update(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    isCompleted = request.POST.get('isCompleted', False)
    if isCompleted == 'on':
        isCompleted = True
    
    todo.isCompleted = isCompleted

    todo.save()
    return redirect('todos:index')