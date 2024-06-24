from django.contrib import admin
from .models import Post, ImagePost, Question, Package, PackagePurchase

#Registro de nuestros modelos:

class ImagePostAdmin(admin.TabularInline): #TabularInline me permite guardar mas de un elemento en linea
    model = ImagePost #Minuto 8 del video para poder continuar


class QuestionInLine(admin.TabularInline):
    model = Question
    extra = 0

class PostAdmin(admin.ModelAdmin): #Exclusivamente para el panel del administrador
    list_display = ["title", "author","category","branch","status"]
    #list_editable = ["title"] -> Si quiero que sea editable
    #search_fields = ["title"]  -> Para buscar por nombre
    #list_filter = ["title"] -> para filtrar
    #list_per_page = 2 -> 2 reg por página
    inlines = [
        QuestionInLine,
        #ImagePostAdmin        
    ]
    

class PackagePurchaseAdmin(admin.ModelAdmin): #Exclusivamente para el panel del administrador
    list_display = ["post", "package","purchase_date","price"]

admin.site.register(Post, PostAdmin)
admin.site.register(Question)
admin.site.register(Package)
admin.site.register(PackagePurchase,PackagePurchaseAdmin)