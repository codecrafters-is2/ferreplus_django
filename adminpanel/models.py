from django.db import models


class Contact(models.Model):
    email = models.EmailField(max_length=254, default="ferreplus@gmail.com")

    def __str__(self):
        return self.email
