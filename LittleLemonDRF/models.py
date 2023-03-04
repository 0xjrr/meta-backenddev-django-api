from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True) #indexed

class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True) #indexed
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True) #indexed
    featured = models.BooleanField(db_index=True) #indexed
    category = models.ForeignKey(Category, on_delete=models.PROTECT)


