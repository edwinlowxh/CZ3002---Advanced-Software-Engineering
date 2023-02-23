from django import forms

from django.contrib.auth.password_validation import validate_password

from user_profile.constants import(
    PASSWORD_CONFIRM_VAR_NAME,
    PASSWORD_VAR_NAME
)

class ChangePasswordForm(forms.Form):
    password = forms.CharField(validators=[validate_password], required=True)
    confirm_password = forms.CharField(required=True)

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
            PASSWORD_VAR_NAME: 'password',
            PASSWORD_CONFIRM_VAR_NAME: 'confirm_password',
        }
        mapped_data = {}
        for key, value in json_data.items():
            if key in mapping:
                mapped_data[mapping[key]] = value
        return mapped_data
