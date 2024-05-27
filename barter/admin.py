from django.contrib import admin
from .models import Barter

class BarterAdmin(admin.ModelAdmin):
    list_display = ["barter_info", "state"]

    def barter_info(self, obj):
        return str(obj) 

    barter_info.short_description = 'Trueque'  # Etiqueta para mostrar en el panel admin

admin.site.register(Barter,BarterAdmin)