from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .utils import sendEmailToClient
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

# Create your views here.

@login_required(login_url='/login/')        #To hide from non-loggedin users
def recipes(request):
    if request.method=="POST":
        data= request.POST

        recipeName=data.get ('recipeName')
        recipeDescription=data.get ('recipeDescription')
        recipeImage=request.FILES.get('recipeImage')

        # print(recipeName)
        # print(recipeDescription)
        # print(recipeImage)

        recipe.objects.create(              #To store the data in db by creating objects
            recipeName=recipeName,
            recipeDescription=recipeDescription,
            recipeImage=recipeImage
        )
        # In shell,
        # >>> from recipeApp.models import *
        # >>> recipe.objects.all()[0].recipeName

        return redirect('/recipes/')    #For warning popup while resubmitting form

    queryset=recipe.objects.all()       #For storing all the datas

    if request.GET.get('search'):       #For searching keywords from the dataset
        queryset=queryset.filter(recipeName__icontains=request.GET.get('search'))
    #'<field>__icontains' is a django keyword to seach in the field

    context={'recipes': queryset}
    return render(request,'recipes.html',context)


@login_required(login_url='/login/')
def deleteRecipe(request,id):
    queryset=recipe.objects.get(id=id)
    queryset.delete()

    return redirect('/recipes/')


@login_required(login_url='/login/')
def updateRecipe(request,id):
    queryset=recipe.objects.get(id=id)
    if request.method=="POST":
        data= request.POST
        recipeName=data.get ('recipeName')
        recipeDescription=data.get ('recipeDescription')
        recipeImage=request.FILES.get('recipeImage')

        queryset.recipeName=recipeName
        queryset.recipeDescription=recipeDescription
        if recipeImage:
            queryset.recipeImage=recipeImage
        
        queryset.save()
        return redirect('/recipes/')

    context={'recipes': queryset}

    return render(request,'updateRecipe.html',context)



def loginPage(request):
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
            login(request, user)
            return redirect('/recipes/')

    return render(request,'login.html')
##SampleUsername: Sarthak22
##SamplePassword: sartt



@login_required(login_url='/login/')
def logoutPage(request):
    logout(request)
    return redirect('/login/') 





def registerPage(request):
    
    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request,'Username Already Taken')
            return redirect('/register/')
        
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            # password=password         #Stores password as string
        )
        user.set_password(password)     #For encrypting the password
        user.save()
        messages.info(request,'Account Created Successfully!')

        return redirect('/register/')

    return render(request,'register.html')

def send_email(request):
    sendEmailToClient()
    return render(request,'email_template.html')

def sendEmailToClient():
    subject = "Demo Email"
    context = {
        'subject': subject,
        'message': "This is a demo email by my Django server"
    }
    html_content = render_to_string('email_template.html', context)
    text_content = strip_tags(html_content)  # Strip the HTML tags for the plain text version

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, ['chakrabortysarthak5@gmail.com'])
    msg.attach_alternative(html_content, "text/html")

    try:
        msg.send()
        print("Email sent successfully.")
    except Exception as e:
        print("An error occurred while sending the email:", e)

