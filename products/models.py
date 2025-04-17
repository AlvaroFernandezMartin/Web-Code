from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('category', 'name')

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.name

    @property
    def category(self):
        return self.subcategory.category
