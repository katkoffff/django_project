from django.db import models
from django.core.validators import MinValueValidator


class Post(models.Model):
    title=models.CharField(
        max_length=50,
        unique=True,
    )
    author=models.CharField(
        max_length=50,
    )
    content=models.TextField()
    category=models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='news'
    )

    def __str__(self):
        return f'{self.title}:{self.author[:20]}'

class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)

    def __str__(self):
        return f'{self.name}'
