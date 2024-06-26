from django import forms
from posts.models import Package, Post, PackagePurchase
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from datetime import datetime

class PaymentForm(forms.ModelForm):
    card_number = forms.CharField(
        max_length=19,
        widget=forms.TextInput(),
        label="Número de Tarjeta"
    )
    expiration_date = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={'placeholder': 'MM/AA'}),
        label="Fecha de vencimiento",
    )
    cvc = forms.CharField(
        max_length=3,
        validators=[RegexValidator(r'^\d{3}$', 'El CVC debe tener 3 dígitos.')],
        widget=forms.TextInput(attrs={'placeholder': '***'}),
        label="CVC",
    )

    package = forms.ModelChoiceField(
        queryset=Package.objects.exclude(name='Ninguno'),
        widget=forms.Select,
        label="Seleccione un paquete",
    )

    class Meta:
        model = PackagePurchase
        fields = ['package', 'card_number', 'expiration_date', 'cvc']

    def __init__(self, post_id, *args, **kwargs):
        self.post_id = post_id
        super().__init__(*args, **kwargs)
        self.fields['package'].label_from_instance = self.label_from_instance

    def label_from_instance(self, obj):
        return f"{obj.get_name_display()} - ${obj.price}"
    
    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        card_number = card_number.replace('-', '')
        if not card_number.isdigit() or len(card_number) != 16:
            raise forms.ValidationError('El número de tarjeta debe tener 16 dígitos.')
        return card_number
    
    def clean_expiration_date(self):
        data = self.cleaned_data.get('expiration_date')

        if '/' not in data or len(data.split('/')) != 2:
            raise ValidationError('La fecha de expiración debe estar en el formato MM/AA.')

        try:
            month, year = data.split('/')
            month = int(month)
            year = int(year)
        except ValueError:
            raise ValidationError('La fecha de expiración debe estar en el formato MM/AA.')

        if month < 1 or month > 12:
            raise ValidationError('El mes de la fecha de expiración debe ser un valor entre 01 y 12.')

        if year < 100:  
            year += 2000

        try:
            exp_date = datetime.strptime(f'{month:02}/{year}', '%m/%Y')
        except ValueError:
            raise ValidationError('La fecha de expiración no es válida.')

        if exp_date < datetime.now():
            raise ValidationError('La fecha de expiración debe ser en el futuro.')

        return data
    
    def clean_package(self):
        post_id = self.post_id
        package = self.cleaned_data.get('package')

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise ValidationError('La publicación especificada no existe')

        if post.package == package:
            raise ValidationError('Esta publicación ya tiene este paquete activo')

        return package