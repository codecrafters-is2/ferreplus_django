from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
#from django.views.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Post, ImagePost

class PostListView(ListView): 
    model = Post
    template_name = "post_list.html"
    
class PostDetailView(DetailView): # Visualización de la publicación
    model = Post
    template_name = "post_detail.html"
    
class PostCreateView(CreateView): #Creación de la publicación
    model = Post, ImagePost
    template_name = "post_new.html"
    fields = ["title", "author", "body","category","new","brand","manufacturing_date","post"]#,"image"]
    #def form_valid(self, form): # Para que ponga el usuario que es, debo de borrar author arriba
        #form.instance.author = self.request.user
        #return super().form_valid(form)
    
class PostUpdateView(UpdateView): #Edición de la publicación
    model = Post
    template_name = "post_edit.html"
    fields = ["title", "body","category","new","brand"]
    
class PostDeleteView(DeleteView): #Eliminación de la publicación
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("post_list")
    
#class ArticleCreateView(LoginRequiredMixin, CreateView):