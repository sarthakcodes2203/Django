from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def todos(request):
    if request.method=="POST":
        data= request.POST

        todoTitle=data.get('todoTitle')
        todoDescription=data.get('todoDescription')

        # print(todoTitle)
        # print(todoDescription)
        todo.objects.create(
            todoTitle=todoTitle,
            todoDescription=todoDescription,
        )

        return redirect('/todos/')
        
    queryset=todo.objects.all()

    if request.GET.get('search'): 
        queryset=queryset.filter(todoTitle__icontains=request.GET.get('search'))
    
    if request.GET.get('search'):
        queryset=queryset.filter(todoTitle__icontains=request.GET.get('search'))

    context={'todos': queryset}
    return render(request,'index.html',context)
















def deleteTodo(request,id):
    queryset=todo.objects.get(id=id)
    queryset.delete()

    return redirect('/todos/')






def updateTodo(request,id):
    queryset=todo.objects.get(id=id)

    if request.method=="POST":
        data= request.POST
        todoTitle=data.get ('todoTitle', '')
        todoDescription=data.get ('todoDescription', '')

        queryset.todoTitle=todoTitle
        queryset.todoDescription=todoDescription
        queryset.save()

        return redirect('/todos/')

    context={'todos': queryset}

    return render(request,'updateTodo.html',context)












def home(request):
    return render(request,'home.html')














def login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request,'Invalid Username ')
            return redirect('/login/')

        user=authenticate(username=username, password=password)
        if user is None:
            messages.error(request,'Invalid Password ')
            return redirect('/login/')

        else:
            return redirect('/todos/')

    return render(request,'login.html')







@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    return redirect('login') 












def signup(request):

    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request,'Username Already Taken')
            return redirect('/signup/')
        
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            # password=password         #Stores password as string
        )
        user.set_password(password)     #For encrypting the password
        user.save()
        messages.info(request,'Account Created Successfully!')

        return redirect('/signup/')

    return render(request,'signup.html')





def signup2(request):
    return render(request,'signup2.html')














