from django import forms

from django.utils.timezone import now

from django.contrib.auth.models import User

from Budget.constants import(
    CATEGORY_NAME_VAR,
    CATEGORY_ID_VAR,
    BUDGET_ID_VAR,
    BUDGET_LIMIT_VAR,
    BUDGET_YEAR_VAR,
    BUDGET_MONTH_VAR
)
from Budget.models import Category, Budget


class CreateBudgetForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    limit = forms.FloatField(required=True, min_value=0.01, max_value=1000000000)
    year = forms.IntegerField(required=True, min_value=1990, max_value=2100)
    month = forms.IntegerField(required=True, min_value=1, max_value=12)
    category = forms.CharField(max_length=255, required=True)
    

    def clean_category(self):
        user = self.cleaned_data["user"]
        category = self.cleaned_data["category"]

        query_set = Category.category_manager.get_categories(user=user, name=category)
        if not query_set:
            raise forms.ValidationError(f"Category {category} does not exist")
        else:
            return query_set[0]   
        

    @staticmethod
    def map_json(json_data):
        mapping = {
            CATEGORY_NAME_VAR: 'category',
            BUDGET_ID_VAR: 'id',
            BUDGET_LIMIT_VAR: 'limit',
            BUDGET_YEAR_VAR: 'year',
            BUDGET_MONTH_VAR: 'month'
        }
        mapped_data = {}
        for key, value in json_data.items():
            if key in mapping:
                mapped_data[mapping[key]] = value
        return mapped_data