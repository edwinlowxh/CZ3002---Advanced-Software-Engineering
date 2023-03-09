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
    type = forms.ChoiceField(choices=[choice for choice in TRANSACTION_TYPE], required=True)
    amount = forms.FloatField(required=True)
    category = forms.CharField(max_length=255, required=False, empty_value=None)
    date = forms.DateField(input_formats=['%d/%m/%Y'], required=False, widget=forms.DateInput)
    description = forms.CharField(max_length=255, required=False, empty_value=None)

    def __init__(self, user: User = None, **kwargs):
        if not user:
            super().__init__(None)
        else:
            super().__init__(kwargs)
        self.user = user

    def clean_date(self):
        date = self.cleaned_data['date']
        
        if not date:
            return now().today()
        else:
            return date

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        category = cleaned_data['category']
        _type = cleaned_data['type']

        if _type == 'EXPENSE':
            if not category:
                self.add_error('category', f"Category cannot be empty for expense")
            else:
                category = self.cleaned_data['category']
                query_set = Category.category_manager.get_categories(user=self.user).filter(name=category)

                if not query_set:
                    self.add_error('category', f"Category {category} does not exist")
                self.data['category'] = query_set[0]
       
    @staticmethod
    def map_fields(json_data: dict, reverse: bool = False):
        if not reverse:
            mapping = {
                CATEGORY_NAME_VAR: 'category',
                TRANSACTION_AMOUNT_VAR: 'amount',
                TRANSACTION_DATE_VAR: 'date',
                TRANSCATION_DESCRIPTION_VAR: 'description',
                TRANSACTION_TYPE_VAR: 'type'
            }
        elif reverse:
            mapping = {
                'category': CATEGORY_NAME_VAR,
                'amount': TRANSACTION_AMOUNT_VAR,
                'date': TRANSACTION_DATE_VAR,
                'description': TRANSCATION_DESCRIPTION_VAR,
                'type': TRANSACTION_TYPE_VAR
            }

        mapped_data = {}
        for key, value in json_data.items():
            if key in mapping:
                mapped_data[mapping[key]] = value
        return mapped_data
