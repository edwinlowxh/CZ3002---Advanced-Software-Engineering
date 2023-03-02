from django.shortcuts import redirect, render

from django.contrib.auth import logout, authenticate, update_session_auth_hash, login as django_login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

from django.views.decorators.csrf import csrf_exempt

from django.forms.models import model_to_dict

from django.http import JsonResponse

from django.db import IntegrityError

from FinApp.decorators import basic_auth

from user_profile.constants import *
from user_profile.models import UserInformation
from user_profile.forms.RegisterForm import RegisterForm
from user_profile.forms.ChangePasswordForm import ChangePasswordForm
from user_profile.forms.UpdateUserInformationForm import UpdateUserInformationForm


# Create your views here.
@csrf_exempt
def register(request):
    if request.method == "POST":
        form_data = RegisterForm.map_json(request.POST.dict())
        form = RegisterForm(form_data)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            try:
                user = User.objects.create_user(username=username, password=password, email=email)
                return JsonResponse({"message": "Successful Registration"})
            except IntegrityError:
                return JsonResponse({"message": "Failed Registration", "error": {"username": "Username taken"}})
        else:
            return JsonResponse({"message": "Failed Registration", "error": form.errors})         
    elif request.method == "GET":
        return JsonResponse({}) 

@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST.get(USERNAME_VAR_NAME)
        password = request.POST.get(PASSWORD_VAR_NAME)
        user = authenticate(username=username, password=password)

        if user is not None:
            django_login(request=request, user=user)
            return redirect('home')

        if user:
            return JsonResponse({"message": "Logged In"})
        else:
            return JsonResponse({"message": "Failed Authentication"})
        
    return render(request, 'accounts/login.html')

@csrf_exempt
def logout(request):
    try:
        # Get the current session key
        session_key = request.session.session_key
        # Delete the session using the session key
        Session.objects.get(session_key=session_key).delete()
        logout(request)
    except:
        pass
    return JsonResponse({"message": "Logged Out"})

@csrf_exempt
@basic_auth
def change_password(request):
    if request.method == "POST":
        if request.user.is_authenticated and request.user.is_active:
            form_data = ChangePasswordForm.map_json(request.POST.dict())
            form = ChangePasswordForm(form_data)
            user = request.user

            if form.is_valid():
                password = form.cleaned_data['password']
                user.password = make_password(password)
                user.save()
                update_session_auth_hash(request, user)
                return JsonResponse({"message": "Password Changed"})
            else:
                return JsonResponse({"message": "Failed to change password", "errors": form.errors})
        else:
            return JsonResponse({"message": "Authentication Failed"})
         
    elif request.method == "GET":
        return JsonResponse({})  

@csrf_exempt
def forget_password(request):
    #send email
    # https://learndjango.com/tutorials/django-password-reset-tutorial
    pass

@csrf_exempt
@basic_auth
def update_user_information(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = request.user
            form_data = UpdateUserInformationForm.map_json(request.POST.dict())
            form = UpdateUserInformationForm(form_data)

            if form.is_valid():         
                print(form.cleaned_data)
                UserInformation.user_information_manager.save_user_information(user, **form.cleaned_data)
                return JsonResponse({"message": "User information saved"})
            else:
                return JsonResponse({"message": "Failed to update user information", "error": form.errors})
        elif request.method == "GET":
            try:
                query_set = UserInformation.user_information_manager.retrieve_user_information(user = request.user)
                user_information = query_set.get(user = request.user)
                return JsonResponse(model_to_dict(user_information))
            except Exception as e:
                print(e)
                return JsonResponse({"message": "Failed to retrieve user information"})
    else:
        return JsonResponse({"message": "Please log in"})


            
            
