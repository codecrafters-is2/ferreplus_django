from django import forms
from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["title","body","category","new","brand","manufacturing_date","image",
                    "author", #Este, tiene que desaparecer despues
                ] #Campos que va a completar el usuario
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
        self.fields["author"].label = "Autor del producto"
        self.fields["category"].label = "Categoría del producto"
        self.fields["new"].label = "Nuevo"
        self.fields["brand"].label = "Marca"
        self.fields["manufacturing_date"].label = "Fecha de creación"
        self.fields["image"].label = "Imagen del producto"
    
    #def clean_images(self):
    #    images = self.cleaned_data.get('images')
    #    if not images:
    #        raise forms.ValidationError("Debe cargar al menos una imagen.")
    #    return images