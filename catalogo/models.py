from django.db import models


class Product(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=150, null=False)
    description = models.TextField(max_length=1000, null=False)
    price = models.FloatField()
    category = models.ForeignKey(to="ProductCategory", null=False, on_delete=models.CASCADE)
    stock = models.IntegerField()  # Stock general ?
    main_image = models.ImageField(upload_to="products_images", null=True, blank=True)
    active = models.BooleanField(default=True)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=150, null=False)
    image = models.ImageField(upload_to="products_images")


class ProductCategory(models.Model):
    name = models.CharField(max_length=150, null=False)
    description = models.CharField(max_length=500, null=True)
    image = models.ImageField(upload_to="categories_images", null=True, blank=True)
