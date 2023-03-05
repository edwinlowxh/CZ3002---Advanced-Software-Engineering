from django.contrib.auth import login, logout, authenticate

from django.http import HttpResponse, HttpRequest

from django.core.handlers.wsgi import WSGIRequest

import base64

from typing import Callable

def basic_auth(view_func: Callable[[HttpRequest], HttpResponse]) -> HttpResponse:
    '''
        Basic Authentication decorator for testing endpoints which requires users to be authenticated.
        Send request with basic authentication (username, password)
        NOTE: Insecure authentication method to only be used in testing
    '''
    def get_basic_auth(request):
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                if auth[0].lower() == "basic":
                    username, password = base64.b64decode(auth[1]).decode('utf-8').split(':')
                    return (username, password), True
        else:
            return None, False

    def check_basic_auth(request):
        credentials, is_basic_auth = get_basic_auth(request)
        if is_basic_auth:
            user = authenticate(username=credentials[0], password=credentials[1])
            if user is not None:
                if user.is_active:
                    login(request, user)

        response = view_func(request)
        return response

    return check_basic_auth
                    
