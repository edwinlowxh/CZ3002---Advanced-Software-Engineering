from django.shortcuts import render

from django.contrib.auth import logout, authenticate, update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt

from django.forms.models import model_to_dict
from django.contrib.sessions.models import Session

from django.http import JsonResponse

from FinApp.decorators import basic_auth

from user_profile.constants import *
from user_profile.models import UserInformation


# Create your views here.
@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST.get(USERNAME_VAR_NAME)
        password = request.POST.get(PASSWORD_VAR_NAME)
        email = request.POST.get(EMAIL_VAR_NAME)
        first_name = request.POST.get(FIRST_NAME_VAR_NAME)
        last_name = request.POST.get(LAST_NAME_VAR_NAME)

        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

        if user:
            return JsonResponse({"message": "Successful Registration"})
        else:
            return JsonResponse({"message": "Failed Registration"})
         
    elif request.method == "GET":
        return JsonResponse({}) 

@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST.get(USERNAME_VAR_NAME)
        password = request.POST.get(PASSWORD_VAR_NAME)
        user = authenticate(username=username, password=password)

        if user:
            return JsonResponse({"message": "Logged In"})
        else:
            return JsonResponse({"message": "Failed Authentication"})
         
    elif request.method == "GET":
        return JsonResponse({})

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
            user = request.user
            password = request.POST.get(PASSWORD_VAR_NAME)
            password_confirm = request.POST.get(PASSWORD_CONFIRM_VAR_NAME)
            user.password = make_password(password)
            user.save()
            update_session_auth_hash(request, user)

            return JsonResponse({"message": "Password Changed"})
        else:
            return JsonResponse({"message": "Authentication Failed"})
         
    elif request.method == "GET":
        return JsonResponse({})  

@csrf_exempt
def forget_password(request):
    #send email
    pass

@csrf_exempt
@basic_auth
def update_user_information(request):
    if request.user.is_authenticated:
        if request.method == "POST":
        
            user = request.user
            day, month, year = request.POST.get(DATE_OF_BIRTH_VAR_NAME).split('/')
            marital_status = request.POST.get(MARITAL_STATUS_VAR_NAME)
            birth_date = (day, month, year)
            try:
                UserInformation.user_information_manager.save_user_information(user, marital_status=marital_status, birth_date=birth_date)
            except Exception as e:
                print(e)
                return JsonResponse({"message": "Failed to save user information"})
            return JsonResponse({"message": "User information saved"})
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


            
            
