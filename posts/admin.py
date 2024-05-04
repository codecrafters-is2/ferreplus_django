from django.contrib import admin
from .models import Post, ImagePost

#Registro de nuestros modelos:

class ImagePostAdmin(admin.TabularInline): #TabularInline me permite guardar mas de un elemento
    model = ImagePost #Minuto 8 del video para poder continuar
    
#Agrega en la clase PostAdmin:
# inlines = [
#   ImagePostAdmin        
#]

    
admin.site.register(Post)