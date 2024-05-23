from django import forms
from .models import Post,ImagePost, Question

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["title","body","image","category","branch","new","brand",
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
        self.fields["category"].label = "Categoría del producto"
        self.fields["new"].label = "Nuevo"
        self.fields["brand"].label = "Marca"
        self.fields["image"].label = "Imagen del producto"
        self.fields["branch"].label= "Sucursal de preferencia"

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['content']#, "answer"
        widgets = {
            'content': forms.Textarea(attrs={'maxlength': 150}),
            #'answer': forms.Textarea(),  # Asegúrate de que el campo de respuesta sea un área de texto
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

#class MultipleFileInput(forms.ClearableFileInput):
#    allow_multiple_selected = True

#class MultipleFileField(forms.FileField):
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

#class FileFieldForm(forms.Form):
#    file_field = MultipleFileField()

#class ImageForm(forms.ModelForm):
#    class Meta:
#        model = ImagePost
#        fields = ['image',]
        #widgets = {
        #    'image': forms.FileInput(attrs={'multiple': True}) -->Falla con esto, por eso se usa MultipleFileField
        #}
        
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


    
    #def clean_images(self):
    #    images = self.cleaned_data.get('images')
    #    if not images:
    #        raise forms.ValidationError("Debe cargar al menos una imagen.")
    #    return images