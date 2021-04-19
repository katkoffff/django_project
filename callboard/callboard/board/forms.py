from django import forms
from .models import Post, Replay
from django.forms import Select, TextInput
from ckeditor.widgets import CKEditorWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'head', 'content']

class ReplayForm(forms.ModelForm):
    class Meta:
        model = Replay
        fields = ['content']


class ConfirmForm(forms.ModelForm):
    class Meta:
        model = Replay
        fields = ['author', 'post', 'content',  'status']


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'head', 'content']
        widgets = {
            'category': Select(attrs={
                'class': 'custom-select',
                'option selected': 'Выбрать тип'
            }),
            'head': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название объявления'
            }),
            'content': CKEditorWidget(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст...'
            }),
        }











