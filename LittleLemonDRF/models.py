from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    slug = models.SlugField()
    tittle = models.CharField(max_length=255, db_index=True) #indexed


