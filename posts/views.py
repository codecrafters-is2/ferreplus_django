from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.forms import inlineformset_factory

from .models import Post, ImagePost
from .forms import PostForm

class PostListView(ListView): 
    model = Post
    template_name = "posts/post_list.html"
    #Por defecto -> queryset = Model.objects.all()
    queryset = Post.objects.filter(status = "available") 
    #queryset = Post.objects.filter(new = True) #Solo se muestran los nuevos
    
class PostDetailView(DetailView): # Visualización de la publicación
    model = Post
    template_name = "posts/post_detail.html"
    
class PostCreateView(CreateView): #Creación de la publicación
    model = Post
    template_name = "posts/post_new.html"
    form_class = PostForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ImageFormSet = inlineformset_factory(Post, ImagePost, fields=('image',), extra=4)
        if self.request.POST:
            context['image_formset'] = ImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['image_formset'] = ImageFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        if image_formset.is_valid():
            self.object = form.save()
            image_formset.instance = self.object
            image_formset.save()
            uploaded_images = self.request.FILES.getlist('photo')
            for image in uploaded_images:
                # Crea una nueva instancia de ImagePost
                image_post = ImagePost(post=self.object, image=image)
                # Guarda la instancia en la base de datos
                image_post.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
        
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request  # Agregar el objeto request al formulario
        return form
    
class PostUpdateView(UpdateView): #Edición de la publicación
    model = Post
    template_name = "posts/post_edit.html"
    #fields = ["title", "body","category","new","brand"]
    form_class = PostForm
    
class PostDeleteView(DeleteView): #Eliminación de la publicación
    model = Post
    template_name = "posts/post_delete.html"
    success_url = reverse_lazy("post_list") #Redirección cuando termina la acción
