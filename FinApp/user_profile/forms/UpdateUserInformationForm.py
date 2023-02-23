from django import forms

from user_profile.constants import(
    MARITAL_STATUS_VAR_NAME,
    DATE_OF_BIRTH_VAR_NAME,
    MARITAL_STATUS_LIST    
)

class UpdateUserInformationForm(forms.Form):
    marital_status = forms.ChoiceField(choices=MARITAL_STATUS_LIST, required=False)
    date_of_birth = forms.DateField(input_formats=['%d/%m/%Y'], required=False)   

    @staticmethod
    def map_json(json_data):
        mapping = {
            MARITAL_STATUS_VAR_NAME: 'marital_status',
            DATE_OF_BIRTH_VAR_NAME: 'date_of_birth',
        }
        mapped_data = {}
        for key, value in json_data.items():
            if key in mapping:
                mapped_data[mapping[key]] = value
        return mapped_data
