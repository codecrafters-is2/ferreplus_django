from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()
#Sucursal = get_sucursales()


class Post(models.Model):
    POST_STATUS_AVAILABLE = 'available'
    POST_STATUS_RESERVED = 'reserved'
    POST_STATUS_COMPLETED = 'completed'
    POST_STATUS_CHOICES = (
        (POST_STATUS_AVAILABLE, 'Disponible'),
        (POST_STATUS_RESERVED, 'Reservado'),
        (POST_STATUS_COMPLETED, 'Finalizado'),
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
    #author = models.ForeignKey( #Muchos a uno, un usuario puede ser autor de muchas publicaciones
    #    "auth.User" --> settings.AUTH_USER_MODEL,#Acá tengo que referenciar al user posta
    #    on_delete=models.CASCADE,
    #)
    author = models.ForeignKey(User, on_delete=models.CASCADE) #Actualizar con lo de arriba cuando este la parte de usuarios lista
    body = models.TextField(blank=True, null=True) #Chequear
    image = models.ImageField(upload_to="post_images") #Para una imagen sola
    category = models.CharField(max_length=22, choices=CHOICES)
    #branch = models.ForeignKey("Sucursal" , on_delete=models.CASCADE) #Sucursal
    #barter = models.ForeignKey("Trueque" , on_delete=models.CASCADE) #Trueque
    #La "pregunta" se tiene que hacer desde su modelo
    related_posts = models.ManyToManyField('self', blank=True, related_name='related_by', editable=False)
    new = models.BooleanField(blank=True, null=True)
    brand = models.CharField(max_length=30,blank=True, null=True) #marca
    status = models.CharField(max_length=20, choices=POST_STATUS_CHOICES, default=POST_STATUS_AVAILABLE, editable=False)
    manufacturing_date = models.DateField(blank=True, null=True)  

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})


class ImagePost(models.Model):#
    image = models.ImageField(upload_to='post_images')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')#related_name es el nombre que tiene la otra entidad para llamarla
    #Falta la limitacion de 1 a 4 imágenes
    
    def __str__(self):
        return f"Imagen de {self.post.title}"

#    class Meta:
#        validators = [
#            # Asegura que cada publicación tenga al menos una imagen
#            MinValueValidator(1, "Cada publicación debe tener al menos una imagen."),
#            # Asegura que cada publicación tenga como máximo cuatro imágenes
#            MaxValueValidator(4, "Cada publicación puede tener como máximo cuatro imágenes.")
#        ]