from django import forms
from branches.models import Branch

class BranchForm(forms.ModelForm):
    
    class Meta:
        model = Branch
        fields = ["city", "address", "postal_code", "phone"]
        labels = {
            "city": "Ciudad",
            "address": "Dirección",
            "postal_code": "Código Postal",
            "phone": "Teléfono"
        }

    def __init__(self, *args, **kwargs):
        super(BranchForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True
    
    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get("city")
        address = cleaned_data.get("address")
        postal_code = cleaned_data.get("postal_code")
        if Branch.objects.filter(city=city, address=address, postal_code=postal_code).exists():
            raise forms.ValidationError("Ya existe una sucursal en esa ubicación.")
        
        return cleaned_data
