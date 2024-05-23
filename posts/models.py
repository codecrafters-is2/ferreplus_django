from django.db import models
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import MaxLengthValidator
from branches.models import Branch

User = get_user_model()

class Post(models.Model):
    POST_STATUS_AVAILABLE = 'available'
    POST_STATUS_RESERVED = 'reserved'
    POST_STATUS_COMPLETED = 'completed'
    POST_STATUS_PAUSED = "paused"
    POST_STATUS_CHOICES = (
        (POST_STATUS_AVAILABLE, 'Disponible'),
        (POST_STATUS_RESERVED, 'Reservado'),
        (POST_STATUS_COMPLETED, 'Finalizado'),
        (POST_STATUS_PAUSED, "Pausado")
    )

    HERRAMIENTAS = "tools" #En la BD su campo se denomina con el String 
    CONSTRUCCION = "construction"
    FERRETERIA_GRAL = "general_hardware_store"
    ELECTRICIDAD = "electrical"
    FONTANERIA = "plumbing"
    JARDIN = "gardens"
    CHOICES = [
        (HERRAMIENTAS, 'Herramientas'),
        (CONSTRUCCION, 'Construcción'),
        (FERRETERIA_GRAL, 'Ferretería general'),
        (ELECTRICIDAD, "Electricidad"),
        (FONTANERIA, 'Fontanería'),
        (JARDIN, 'Jardin'),
    ]
    
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    body = models.TextField(blank=True, null=True) 
    image = models.ImageField(upload_to="post_images") #Para una imagen sola
    category = models.CharField(max_length=22, choices=CHOICES)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL,null=True) #Sucursal
    original_branch_id = models.IntegerField(null=True) #ID sucursal original para cuando eliminamos una sucursal y la publi se ponga en pausado
    #barter = models.ForeignKey("Trueque" , on_delete=models.CASCADE) #Trueque
    #La "pregunta" se tiene que hacer desde su modelo
    related_posts = models.ManyToManyField('self', blank=True, related_name='related_by', editable=False)
    new = models.BooleanField(blank=True, null=True)
    brand = models.CharField(max_length=30,blank=True, null=True) #marca
    status = models.CharField(max_length=20, choices=POST_STATUS_CHOICES, default=POST_STATUS_AVAILABLE,) 

    def has_unanswered_questions(self):
        return self.questions.filter(Q(answer__isnull=True) | Q(answer='')).exists()
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

class Question(models.Model): 
    post = models.ForeignKey(Post, related_name='questions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(validators=[MaxLengthValidator(150)])
    created_at = models.DateTimeField(auto_now_add=True)
    #Como va a ser siempre el dueño de la publicación el que responda la pregunta no necesito hacer una clase nueva
    answer = models.TextField(validators=[MaxLengthValidator(150)],blank=True, null=True)
    
    def __str__(self):
        return f'Question by {self.user.username} on {self.post.title}'





#Para cuando podamos cargar mas imagenes
class ImagePost(models.Model):#
    image = models.ImageField(upload_to='post_images')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', max_length=4)#related_name es el nombre que tiene la otra entidad para llamarla
    #Falta la limitacion de 1 a 4 imágenes
    
    def __str__(self):
        return f"Imagen de {self.post.title}"