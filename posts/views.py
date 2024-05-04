from django.views.generic import ListView, DetailView
from .models import Post

class BlogListView(ListView): #Lo arme por el libro, pero es para ponerlo al inicio y no quiero eso, va en otra pagina creo
    model = Post
    template_name = "home.html"
    
class BlogDetailView(DetailView): # new
    model = Post
    template_name = "post_detail.html"