from django.forms import ModelForm
from .models import Post
from django.forms import Select, TextInput, SelectMultiple, Textarea

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['to_author', 'category_post', 'to_category', 'header_post', 'content_post']
        widgets = {
            'header_post': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название статьи или новости'
            }),
            'category_post': Select(attrs={
                'class': 'custom-select',
                'option selected': 'Выбрать тип'
            }),
            'content_post': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст...'
            }),
            'to_author': Select(attrs={
                'class': 'custom-select',
                'option selected': 'Выбрать автора'
            }),
            'to_category': SelectMultiple(attrs={
                'multiple class': 'form-control',
            }),
        }