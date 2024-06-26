from django.db import models
from django.utils import timezone
from django.apps import apps
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator
from branches.models import Branch

User = get_user_model()

class Package(models.Model):
    PACKAGE_NONE = 'Ninguno'
    PACKAGE_BRONCE = 'Bronce'
    PACKAGE_PLATA = 'Plata'
    PACKAGE_ORO = 'Oro'
    PACKAGE_CHOICES = [
        (PACKAGE_NONE, 'Ninguno'),
        (PACKAGE_BRONCE, 'Bronce'),
        (PACKAGE_PLATA, 'Plata'),
        (PACKAGE_ORO, 'Oro'),
    ]
    name = models.CharField(max_length=10, choices=PACKAGE_CHOICES, unique=True,default=PACKAGE_NONE)
    price = models.DecimalField(max_digits=6, decimal_places=2)  # Precio del paquete
    priority = models.IntegerField(default=5) #Para ordenamiento de publicaciones

    def __str__(self):
        return self.get_name_display()

class Post(models.Model):
    POST_STATUS_AVAILABLE = 'available'
    POST_STATUS_RESERVED = 'reserved'
    POST_STATUS_COMPLETED = 'completed'
    POST_STATUS_PAUSED = "paused"
    POST_STATUS_DELETED = "deleted"
    POST_STATUS_CHOICES = (
        (POST_STATUS_AVAILABLE, 'Disponible'),
        (POST_STATUS_RESERVED, 'Reservado'),
        (POST_STATUS_COMPLETED, 'Finalizado'),
        (POST_STATUS_PAUSED, "Pausado"),
        (POST_STATUS_DELETED, "Eliminado")
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
    
    title = models.CharField(max_length=50,verbose_name="Titulo")
    author = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="Autor") 
    body = models.TextField(blank=True, null=True) 
    image = models.ImageField(upload_to="post_images") #Para una imagen sola
    category = models.CharField(max_length=22, choices=CHOICES,verbose_name="Categoría")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL,null=True,verbose_name="Sucursal") #Sucursal
    original_branch_id = models.IntegerField(null=True) #ID sucursal original para cuando eliminamos una sucursal y la publi se ponga en pausado
    new = models.BooleanField(blank=True, null=True,)
    brand = models.CharField(max_length=30,blank=True, null=True,verbose_name="Marca") #marca
    status = models.CharField(max_length=20, choices=POST_STATUS_CHOICES, default=POST_STATUS_AVAILABLE,) 
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Paquete")
    package_start_date = models.DateTimeField(null=True, blank=True)  # Fecha de inicio del paquete
    
    def has_unanswered_questions(self):
        return self.questions.filter(Q(answer__isnull=True) | Q(answer='')).exists()
    
    def __str__(self):
        return self.title
    
    def complete_post(self):
        self.status = 'completed'
        self.save()

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})
    
    def reserve_post(self):
        Barter = apps.get_model('barter', 'Barter')
        
        self.status='reserved'
        self.save()
        
        # Cancelar todos los trueques donde esta publicación está involucrada y no están ya cancelados
        self.requesting_barters.filter(~Q(state=Barter.BARTER_STATE_CANCELLED)).update(state=Barter.BARTER_STATE_CANCELLED)
        self.requested_barters.filter(~Q(state=Barter.BARTER_STATE_CANCELLED)).update(state=Barter.BARTER_STATE_CANCELLED)
    
    def delete_post(self):
        Barter = apps.get_model('barter', 'Barter')
        self.status = self.POST_STATUS_DELETED
        self.save()
        Barter.objects.filter(Q(requesting_post=self) | Q(requested_post=self)).exclude(state=Barter.BARTER_STATE_CANCELLED).update(state=Barter.BARTER_STATE_CANCELLED)
    
    def free_post(self):
        self.status = 'available'
        self.save()
    
    def change_package(self, new_package):
        """
        Cambia el paquete asociado a la publicación y guarda la transacción en la tabla de PackagePurchase.
        """
        # Guardar la fecha de inicio del nuevo paquete
        self.package_start_date = timezone.now()
        # Registrar la transacción de compra
        PackagePurchase.objects.create(
            post=self,
            package=new_package,
            price=new_package.price  
        )
        # Actualizar el paquete
        self.package = new_package
        self.save() 

class Question(models.Model): 
    post = models.ForeignKey(Post, related_name='questions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(validators=[MaxLengthValidator(150)])
    created_at = models.DateTimeField(auto_now_add=True)
    #Como va a ser siempre el dueño de la publicación el que responda la pregunta no necesito hacer una clase nueva
    answer = models.TextField(validators=[MaxLengthValidator(150)],blank=True, null=True)
    
    def __str__(self):
        return f'Question by {self.user.username} on {self.post.title}'

class PackagePurchase(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,verbose_name="Publicación")
    package = models.ForeignKey(Package, on_delete=models.CASCADE,verbose_name="Paquete")
    purchase_date = models.DateTimeField(auto_now_add=True,verbose_name="Fecha")
    price = models.DecimalField(max_digits=6, decimal_places=2,verbose_name="Precio")

    def __str__(self):
        return f"{self.post.title} - {self.package.name} - {self.price}"

#Para cuando podamos cargar mas imagenes
class ImagePost(models.Model):#
    image = models.ImageField(upload_to='post_images')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', max_length=4)#related_name es el nombre que tiene la otra entidad para llamarla
    #Falta la limitacion de 1 a 4 imágenes
    
    def __str__(self):
        return f"Imagen de {self.post.title}"