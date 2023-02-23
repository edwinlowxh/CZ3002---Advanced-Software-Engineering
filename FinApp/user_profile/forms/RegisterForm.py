from django import forms

from django.contrib.auth.password_validation import validate_password

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

def validate_username(value):
    blacklist = ['admin', 'root', 'superuser']
    if value in blacklist:
        raise forms.ValidationError('This username is not allowed.')


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=255, 
        validators=[RegexValidator(regex=r'^\w+$', message='Username can only contain letters, numbers and underscores.'), validate_username],
        required=True
    )
    password = forms.CharField(validators=[validate_password], required=True)
    confirm_password = forms.CharField(required=True)
    email = forms.CharField(validators=[validate_email])

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        else:
            return confirm_password

    @staticmethod
    def map_json(json_data):
        mapping = {
            USERNAME_VAR_NAME: 'username',
            PASSWORD_VAR_NAME: 'password',
            PASSWORD_CONFIRM_VAR_NAME: 'confirm_password',
            EMAIL_VAR_NAME: 'email',
        }
        mapped_data = {}
        for key, value in json_data.items():
            if key in mapping:
                mapped_data[mapping[key]] = value
        return mapped_data
