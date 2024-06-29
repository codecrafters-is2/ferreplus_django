from django import forms
from .models import Post,ImagePost, Question, Package

class UpdatePackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['price']
    
    def __init__(self, *args, **kwargs):
        self.post_instance = kwargs.get('instance')  # Almacena la instancia del post
        super(UpdatePackageForm, self).__init__(*args, **kwargs)
        self.fields["price"].label = "Precio"

    def clean(self):
        cleaned_data = super().clean()
        new_price = cleaned_data.get('price')
        package_instance = self.instance
        
        # Compara el nuevo paquete con el paquete actual del post
        if self.post_instance and new_price == self.post_instance.price:
            raise forms.ValidationError("No puedes elegir el mismo precio que ya está asignado.")
        
        # Mapa de restricciones para validar diferencias de precios entre paquetes
        price_restrictions = {
            'oro': {'min_price': Package.objects.get(name='plata').price},
            'plata': {'min_price': Package.objects.get(name='bronce').price, 'max_price': Package.objects.get(name='oro').price},
            'bronce': {'min_price': Package.objects.get(name='none').price, 'max_price': Package.objects.get(name='plata').price}, 
        }

        # Validar restricciones
        if package_instance.name in price_restrictions:  # Usa el nombre de la instancia del objeto para obtener el nombre del paquete
            # Validación de no igualdad y restricciones de mínimo y máximo
            if 'min_price' in price_restrictions[package_instance.name]:
                if new_price == price_restrictions[package_instance.name]['min_price']:
                    raise forms.ValidationError(f"El precio del paquete '{package_instance.get_name_display()}' no puede ser igual al del paquete anterior.")

                if new_price < price_restrictions[package_instance.name]['min_price']:
                    raise forms.ValidationError(f"El precio del paquete '{package_instance.get_name_display()}' debe ser mayor que el del paquete anterior.")

            if 'max_price' in price_restrictions[package_instance.name]:
                if new_price == price_restrictions[package_instance.name]['max_price']:
                    raise forms.ValidationError(f"El precio del paquete '{package_instance.get_name_display()}' no puede ser igual al del siguiente paquete.")

                if new_price > price_restrictions[package_instance.name]['max_price']:
                    raise forms.ValidationError(f"El precio del paquete '{package_instance.get_name_display()}' debe ser menor que el del siguiente paquete.")

        return cleaned_data


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["title","body","image","category","branch","new","brand", ] #Campos que va a completar el usuario
        widgets = {
            "title" : forms.TextInput(
                attrs= {
                    "class" : "forms-control",
                    "placeholder" : "Ingrese nombre"
                }
            )
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["title"].label = "Nombre del producto"
        self.fields["body"].label = "Descripción del producto"
        self.fields["category"].label = "Categoría del producto"
        self.fields["new"].label = "Nuevo"
        self.fields["brand"].label = "Marca"
        self.fields["image"].label = "Imagen del producto"
        self.fields["branch"].label= "Sucursal de preferencia"
        self.fields["branch"].queryset = Branch.objects.filter(is_active=True)

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'maxlength': 150}),
            
        }
        help_texts = {
            'content': 'Máximo 150 caracteres.',
        }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["content"].label = ""

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['answer']
        widgets = {
            'answer': forms.Textarea(attrs={'maxlength': 150})
        }
        help_texts = {
            'answer': 'Máximo 150 caracteres.',
        }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["answer"].label = ""
from .models import Post,ImagePost
from branches.models import Branch

# class MultipleFileInput(forms.ClearableFileInput):
#    allow_multiple_selected = True

# class MultipleFileField(forms.FileField):
#    def __init__(self, *args, **kwargs):
#        kwargs.setdefault("widget", MultipleFileInput())
#        super().__init__(*args, **kwargs)

#    def clean(self, data, initial=None):
#        single_file_clean = super().clean
#        if isinstance(data, (list, tuple)):
#            result = [single_file_clean(d, initial) for d in data]
#        else:
#            result = [single_file_clean(data, initial)]
#        return result

# class FileFieldForm(forms.Form):
#    file_field = MultipleFileField()

# class ImageForm(forms.ModelForm):
#    class Meta:
#        model = ImagePost
#        fields = ['image',]
# widgets = {
#    'image': forms.FileInput(attrs={'multiple': True}) -->Falla con esto, por eso se usa MultipleFileField
# }

#    def form_valid(self, form):
#        files = form.cleaned_data["file_field"]
#        for f in files:
#            if form.cleaned_data:
#                    image = form.cleaned_data['image']
#                    instance = ImagePost(image=image, post=self.object)
#                    instance.save()
#        return super().form_valid(form)

#    def __init__(self,*args,**kwargs):
#        super().__init__(*args,**kwargs)
#        self.fields["image"].label = "Imagen "
#
#    def clean_image(self): #No chequea un choto
#        images = self.cleaned_data_data.get['image']
#        if len(images) < 1:
#            raise forms.ValidationError("Debes subir al menos una imagen.")
#        if len(images) > 4:
#            raise forms.ValidationError("Solo puedes subir un máximo de 4 imágenes.")
#        return images

# def clean_images(self):
#    images = self.cleaned_data.get('images')
#    if not images:
#        raise forms.ValidationError("Debe cargar al menos una imagen.")
#    return images
