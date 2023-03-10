from django import forms

from django.contrib.auth.password_validation import validate_password

from django.contrib.auth.models import User

from django.core.validators import (
    validate_email,
    RegexValidator
)

from user_profile.constants import(
    EMAIL_VAR_NAME,
    USERNAME_VAR_NAME,
    PASSWORD_CONFIRM_VAR_NAME,
    PASSWORD_VAR_NAME
)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=255, 
        validators=[RegexValidator(regex=r'^\w+$', message='Username can only contain letters, numbers and underscores.')],
        required=True
    )
    password = forms.CharField(required=True)
    confirm_password = forms.CharField(required=True)
    email = forms.CharField(validators=[validate_email])

    def clean_username(self):
        blacklist = ['admin', 'root', 'superuser']
        username = self.cleaned_data['username']

        if username in blacklist:
            raise forms.ValidationError('This username is not allowed.')

        if username in User.objects.values_list('username', flat=True):
            raise forms.ValidationError('Username Taken')
        
        return username
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']

        if not password:
            self.add_error('password', 'Password cannot be empty')
        
        try:
            validate_password(self.cleaned_data['password'])
        except forms.ValidationError as e:
            for error in e:
                self.add_error('password', error)
        
        confirm_password = cleaned_data['confirm_password']

        if not confirm_password:
            self.add_error('confirm_password', 'Confirm Password cannot be empty')
        
        if password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')
               

    @staticmethod
    def map_fields(json_data, reverse: bool=False):
        if not reverse:
            mapping = {
                USERNAME_VAR_NAME: 'username',
                PASSWORD_VAR_NAME: 'password',
                PASSWORD_CONFIRM_VAR_NAME: 'confirm_password',
                EMAIL_VAR_NAME: 'email',
            }
        else:
            mapping = {
                'username': USERNAME_VAR_NAME,
                'password': PASSWORD_VAR_NAME,
                'confirm_password': PASSWORD_CONFIRM_VAR_NAME,
                'email': EMAIL_VAR_NAME,
            }

        mapped_data = {}
        for key, value in json_data.items():
            if key in mapping:
                mapped_data[mapping[key]] = value
        return mapped_data
