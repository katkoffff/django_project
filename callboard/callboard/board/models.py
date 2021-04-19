from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'


class Post(models.Model):
    tank, healer, dd, dealer, guildmasters, questgivers, blacksmiths, leatherworkers, potionmakers, spellmasters = \
        'BM', 'HL', 'DD', 'DL', 'GM', 'QG', 'BS', 'LW', 'PM', 'MS'
    CATEGORYS=[(tank, 'Танки'), (healer, 'Хилы'), (dd, 'ДД'), (dealer, 'Торговцы'), (guildmasters, 'Гилдмастеры'),
               (questgivers,'Квестгиверы'), (blacksmiths, 'Кузнецы'), (leatherworkers, 'Кожевники'),
               (potionmakers, 'Зельевары'), (spellmasters, 'Мастера заклинаний')]
    create = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    head = models.CharField(max_length=255)
    content = RichTextField()
    category = models.CharField(max_length=2,
                                     choices=CATEGORYS,
                                     default=tank)

    def get_absolute_url(self):
        return f'/board/{self.id}'


class Replay(models.Model):
    wait, confirmed, rejected = 'WT', 'CF', 'RJ'
    CATEGORYS = [(wait, 'wait'), (confirmed, 'confirmed'), (rejected, 'rejected')]
    create = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    status = models.CharField(max_length=2,
                                     choices=CATEGORYS,
                                     default=wait)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)