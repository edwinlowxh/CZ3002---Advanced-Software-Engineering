from django import forms

from django.utils.timezone import now

from django.contrib.auth.models import User

from Budget.constants import(
     CATEGORY_NAME_VAR
)
from Budget.models import Category

class CreateCategoryForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    name = forms.CharField(max_length=255, required=True)
    
    def __init__(self, update: bool=False, **kwargs):
        super(CreateCategoryForm, self).__init__(kwargs)
        self.update = update

    def clean_name(self):
        name = self.cleaned_data['name']
        user = self.cleaned_data['user']
        query_set = Category.category_manager.get_categories(user=user, name=name)

        if not self.update:
            if query_set and query_set[0].is_active == True:
                raise forms.ValidationError(f"Category {name} already exists! ")
        else:
            return name
        
        #if query_set and query_set[0].is_active == False:
            #raise forms.ValidationError(f"Category {name} already exists but is not active... ")
            
        return name


    @staticmethod
    def map_fields(json_data, reverse=False):
        if not reverse:
            mapping = {
                CATEGORY_NAME_VAR: 'name'
            }
        else:
            mapping = {
                'name': CATEGORY_NAME_VAR
            }
            
        mapped_data = {}
        for key, value in json_data.items():
            if key in mapping:
                mapped_data[mapping[key]] = value
        return mapped_data
