from django import forms

from django.utils.timezone import now

from django.contrib.auth.models import User

from Transaction.constants import(
    TRANSACTION_TYPE,
    TRANSACTION_AMOUNT_VAR,
    TRANSACTION_DATE_VAR,
    TRANSACTION_TYPE_VAR,
    TRANSCATION_DESCRIPTION_VAR
)

from Budget.constants import(
    CATEGORY_NAME_VAR
)

from Budget.models import Category

class CreateTransactionForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    type = forms.ChoiceField(choices=[choice for choice in TRANSACTION_TYPE], required=True)
    amount = forms.CharField(required=True)
    category = forms.CharField(max_length=255, required=False)
    date = forms.DateField(input_formats=['%d/%m/%Y'], required=False)
    description = forms.CharField(max_length=255, required=False)


    def clean_date(self):
        date = self.cleaned_data['date']
        
        if not date:
            return now().today()
        else:
            return date

    def clean_category(self):
        category = self.cleaned_data['category']
        _type = self.cleaned_data['type']

        if _type == 'EXPENSE':
            if not category:
                raise forms.ValidationError(f"Please provide a category for expense")
            else:
                category = self.cleaned_data['category']
                user = self.cleaned_data['user']
                query_set = Category.category_manager.get_categories(user=user).filter(name=category)

                if not query_set:
                    raise forms.ValidationError(f"Category {category} does not exist")
                else:
                    return query_set[0]          
        else:
            return None


    @staticmethod
    def map_json(json_data):
        mapping = {
            CATEGORY_NAME_VAR: 'category',
            TRANSACTION_AMOUNT_VAR: 'amount',
            TRANSACTION_DATE_VAR: 'date',
            TRANSCATION_DESCRIPTION_VAR: 'description',
            TRANSACTION_TYPE_VAR: 'type'
        }
        mapped_data = {}
        for key, value in json_data.items():
            if key in mapping:
                mapped_data[mapping[key]] = value
        return mapped_data
