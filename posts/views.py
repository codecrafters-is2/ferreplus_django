# Django
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.db.models import Q,F

from django.urls import reverse_lazy
from django.urls import reverse
from django.shortcuts import redirect,get_object_or_404
from django.http import Http404,HttpResponseRedirect
# Local
from accounts.mixins import ClientRequiredMixin, AdminRequiredMixin
from .forms import QuestionForm, AnswerForm
from .models import Post, ImagePost, Question, Package
from .forms import PostForm, ChangePackageForm, UpdatePackageForm
from .services import get_active_posts

#Preguntas de las publicaciones:
class DeleteQuestionView(ClientRequiredMixin, View):
    model = Question

    def post(self, request, *args, **kwargs):
        question_id = kwargs.get('question_id')
        question = get_object_or_404(Question, id=question_id)

        # Elimina la pregunta
        if request.user == question.user:
            question.delete()

        # Redirige a la página de detalle de la publicación
        return redirect('post_detail', pk=question.post.pk)

class DeleteAnswerView(ClientRequiredMixin, View):
    model = Question

    def post(self, request, *args, **kwargs):
        question_id = kwargs.get('question_id')
        question = get_object_or_404(Question, id=question_id)

        # Verifica que el usuario sea el autor de la publicación
        if request.user == question.post.author:
            # Elimina la respuesta
            question.answer = None
            question.save()

        # Redirige a la página de detalle de la publicación
        return redirect('post_detail', pk=question.post.pk)


#Paquetes de las publicaciones:
class ChangePackageView(ClientRequiredMixin,UpdateView):
    model = Post
    template_name = "posts/change_package.html"
    form_class = ChangePackageForm
    
    def get_success_url(self):
        return reverse_lazy('my_post_detail', kwargs={'pk': self.object.pk})


class PackageListView(AdminRequiredMixin, ListView):
    model = Package
    template_name = "packages/package_list.html"
    context_object_name = 'packages'


class UpdatePackageView(AdminRequiredMixin, UpdateView):
    model = Package
    form_class = UpdatePackageForm
    template_name = "packages/update_package.html"
    success_url = reverse_lazy('package_list')  


#Publicaciones:

class PostListView(ClientRequiredMixin,ListView):
    model = Post
    template_name = "posts/list/post_list.html"
    
    def get_queryset(self):
        # Obtener todas las publicaciones
        queryset = super().get_queryset().filter(status="available").exclude(author=self.request.user) #Por defecto -> queryset = Model.objects.all()
        queryset = queryset.annotate(
            package_priority=F('package__priority')  # Anotar con el valor del campo `priority` de `package`
        ).order_by('package_priority', 'title')
        return queryset


class MyPostListView(ClientRequiredMixin,ListView): 
    model = Post
    template_name = "posts/list/my_post_list.html"
    context_object_name = "post_list"  # Cambia el nombre del contexto para que coincida con la plantilla
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            author=self.request.user,
            status__in=[
                Post.POST_STATUS_AVAILABLE,
                Post.POST_STATUS_PAUSED,
                Post.POST_STATUS_RESERVED
            ]
        )
        return queryset


class PostDetailView(ClientRequiredMixin,DetailView): 
    model = Post
    template_name = "posts/detail/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = QuestionForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.post = self.object
            question.save()
            return redirect(self.object.get_absolute_url())
        return self.render_to_response(self.get_context_data(form=form))

    def dispatch(self, request, *args, **kwargs):
        # Obtiene la instancia del post
        self.object = self.get_object()
        # Comprueba si el usuario actual es el autor del post
        if self.object.author == request.user:
            # Si es el autor, redirige a la vista de detalle de su propio post
            return redirect('my_post_detail', pk=self.object.pk)
        # Si no es el autor, permite el acceso normal a la vista de detalle del post
        return super().dispatch(request, *args, **kwargs)

class MyPostDetailView(ClientRequiredMixin,DetailView): #Visualización de la publicación propia
    model = Post
    template_name = "posts/detail/my_post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        # Verificar si el usuario actual es el autor de la publicación
        if self.request.user == post.author:
            # Obtén todas las preguntas asociadas a esta publicación
            questions = post.questions.all()
            questions_with_forms = []
            for question in questions:
                # Crear una instancia de AnswerForm y vincularla a la pregunta actual
                answer_form = AnswerForm(prefix=str(question.id), initial={'question_id': question.id})
                questions_with_forms.append((question, answer_form))
            context['questions_with_forms'] = questions_with_forms
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        post = self.object
        # Itera sobre todas las preguntas y sus respectivos formularios de respuesta
        for question in post.questions.all():
            # Obtiene el prefijo del formulario que corresponde a esta pregunta
            prefix = str(question.id)
            form = AnswerForm(request.POST, prefix=prefix)
            # Verifica si el formulario es válido y ha sido enviado para esta pregunta específica
            if form.is_valid() and f'{prefix}-answer' in request.POST:
                # Guarda la respuesta en la pregunta correspondiente
                answer_text = form.cleaned_data['answer']
                question.answer = answer_text
                question.save()
                break # Sal del bucle después de procesar el formulario enviado
        # Después de procesar todas las respuestas, redirige de vuelta a la vista de detalle del post
        return HttpResponseRedirect(reverse('my_post_detail', kwargs={'pk': self.object.pk}))

    def dispatch(self, request, *args, **kwargs):
        # Obtiene la instancia del post
        self.object = self.get_object()
        # Comprueba si el usuario actual es el autor del post
        if self.object.author != request.user:
            # Si el usuario no es el autor, la abre como si la estuviera visualizando
            return redirect('post_detail', pk=self.object.pk)
        # Si el usuario es el autor, permite el acceso normal a la vista
        return super().dispatch(request, *args, **kwargs)


class PostCreateView(ClientRequiredMixin,CreateView): #Creación de la publicación
    model = Post
    template_name = "posts/post_new.html"
    form_class = PostForm

    def get_success_url(self):
        return reverse_lazy('my_post_detail', kwargs={'pk': self.object.pk})
    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    ImageFormSet = inlineformset_factory(Post, ImagePost, fields=('image',), extra=4)
    #    if self.request.POST:
    #        context['image_formset'] = ImageFormSet(self.request.POST, self.request.FILES)
    #    else:
    #        context['image_formset'] = ImageFormSet()
    #    return context

    def form_valid(self, form):
        # Agrega el campo original_branch_id antes de guardar el formulario
        form.instance.original_branch_id = form.instance.branch.id
        # Asigna el autor actualmente autenticado
        form.instance.author = self.request.user  
        
        #context = self.get_context_data()
        #image_formset = context['image_formset']
        #if image_formset.is_valid():
        #    self.object = form.save()
        #    image_formset.instance = self.object
        #    image_formset.save()
        #    uploaded_images = self.request.FILES.getlist('photo')
        #    for image in uploaded_images:
                # Crea una nueva instancia de ImagePost
        #        image_post = ImagePost(post=self.object, image=image)
                # Guarda la instancia en la base de datos
        #        image_post.save()
        return super().form_valid(form)
        #else:
        #    return self.form_invalid(form)
        
    #def get_form(self, form_class=None):
    #    form = super().get_form(form_class)
    #    form.request = self.request  # Agregar el objeto request al formulario
    #    return form
    
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
    
    def get_success_url(self):
        return reverse_lazy('my_post_detail', kwargs={'pk': self.object.pk})
    
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            raise Http404("No tienes permiso para editar esta publicación.")
        return super().dispatch(request, *args, **kwargs)

class PostDeleteView(ClientRequiredMixin,DeleteView): #Eliminación de la publicación
    model = Post
    template_name = "posts/post_delete.html"
    success_url = reverse_lazy("my_post_list") #Redirección cuando termina la acción
    
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            raise Http404("No tienes permiso para eliminar esta publicación.")

        # Verifica el estado del post
        if self.get_object().status not in [Post.POST_STATUS_AVAILABLE, Post.POST_STATUS_PAUSED]:
            raise Http404("No se puede eliminar la publicación debido a que la misma se encuentra en un trueque confimado.")

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        if post.author != request.user:
            raise Http404("No tienes permiso para eliminar esta publicación.")
        post.delete_post()
        return redirect("my_post_list")


class PostSearchView(ClientRequiredMixin,ListView):
    model = Post
    context_object_name = "post_list"
    template_name = "posts/list/post_list.html"

    def get_queryset(self):
        queryset = get_active_posts().exclude(author=self.request.user)
        query_params = self._get_query_params()

        title_query = query_params.get("title")
        if title_query:
            queryset = queryset.filter(
                Q(title__contains=title_query) | Q(body__contains=title_query)
            )

        categories_query = query_params.get("categories")
        if categories_query:
            queryset = queryset.filter(category__in=categories_query)

        branch_query = query_params.get("branches")
        if branch_query:
            queryset = queryset.filter(branch__id=branch_query)

        queryset = queryset.annotate(
            package_priority=F('package__priority')  
        ).order_by('package_priority', 'title')
        return queryset

    def get_context_data(self, **kwargs):
        """ Datos adicionales para los filtros """
        context = super().get_context_data()
        query_params = self._get_query_params()
        context["active_filters"] = query_params
        return context

    def _get_query_params(self):
        title_query = self.request.GET.get("title")

        raw_categories_query = self.request.GET.get("categories")
        if raw_categories_query:
            categories_query = raw_categories_query.split(",")
        else:
            categories_query = ""

        branch_query = self.request.GET.get("branches")

        return {
            "title": title_query,
            "categories": categories_query,
            "branches": branch_query
        }
