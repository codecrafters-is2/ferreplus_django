from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Post
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
    #fields = ["title", "author", "body","category","new","brand","manufacturing_date"]#,"image"]
    #def form_valid(self, form): # Para que ponga el usuario que es, debo de borrar author arriba
        #form.instance.author = self.request.user
        #return super().form_valid(form)
    
class PostUpdateView(UpdateView): #Edición de la publicación
    model = Post
    template_name = "posts/post_edit.html"
    #fields = ["title", "body","category","new","brand"]
    form_class = PostForm
    
class PostDeleteView(DeleteView): #Eliminación de la publicación
    model = Post
    template_name = "posts/post_delete.html"
    success_url = reverse_lazy("post_list") #Redirección cuando termina la acción
    
