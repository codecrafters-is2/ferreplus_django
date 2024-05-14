from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.http import Http404
from accounts.mixins import ClientRequiredMixin

from .models import Post, ImagePost
from .forms import PostForm

class PostListView(ClientRequiredMixin,ListView): 
    model = Post
    template_name = "posts/post_list.html"
    
    def get_queryset(self):
        # Obtener todas las publicaciones
        queryset = super().get_queryset()
        # Aplicar filtro para obtener solo las publicaciones disponibles
        queryset = queryset.filter(status="available") #Por defecto -> queryset = Model.objects.all()
        # Excluir las publicaciones del usuario actual
        queryset = queryset.exclude(author=self.request.user)
        return queryset


class MyPostListView(ClientRequiredMixin,ListView): 
    model = Post
    template_name = "posts/my_post_list.html"
    context_object_name = "post_list"  # Cambia el nombre del contexto para que coincida con la plantilla
    
    def get_queryset(self):
        # Filtrar las publicaciones por el autor que coincide con el usuario actual
        return Post.objects.filter(author=self.request.user)


class PostDetailView(ClientRequiredMixin,DetailView): # Visualización de la publicación
    model = Post
    template_name = "posts/post_detail.html"


class MyPostDetailView(ClientRequiredMixin,DetailView): #Visualización de la publicación propia
    model = Post
    template_name = "posts/my_post_detail.html"


class PostCreateView(ClientRequiredMixin,CreateView): #Creación de la publicación
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
        # Agrega el campo original_branch_id antes de guardar el formulario
        form.instance.original_branch_id = form.instance.branch.id
        # Asigna el autor actualmente autenticado
        form.instance.author = self.request.user  
        
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
    
class PostUpdateView(ClientRequiredMixin,UpdateView): #Edición de la publicación
    model = Post
    template_name = "posts/post_edit.html"
    #fields = ["title", "body","category","new","brand"]
    form_class = PostForm
    
    def form_valid(self, form):
        # Agrega el campo original_branch_id antes de guardar el formulario
        form.instance.original_branch_id = form.instance.branch.id
        # Actualiza el estado de la publicación
        form.instance.status=Post.POST_STATUS_AVAILABLE
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            raise Http404("No tienes permiso para editar esta publicación.")
        return super().dispatch(request, *args, **kwargs)

class PostDeleteView(ClientRequiredMixin,DeleteView): #Eliminación de la publicación
    model = Post
    template_name = "posts/post_delete.html"
    success_url = reverse_lazy("post_list") #Redirección cuando termina la acción
    
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            raise Http404("No tienes permiso para eliminar esta publicación.")
        return super().dispatch(request, *args, **kwargs)
