from django import forms
from branches.models import Branch

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ["city", "address", "postal_code"]
        labels = {
            "city": "Ciudad",
            "address": "Dirección",
            "postal_code": "Código Postal"
        }

    def __init__(self, *args, **kwargs):
        super(BranchForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True
