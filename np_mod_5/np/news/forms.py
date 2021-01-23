from django.forms import ModelForm, BooleanField
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['to_author', 'category_post', 'header_post', 'content_post']