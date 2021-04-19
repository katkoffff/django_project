#from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
import datetime
from django.core.paginator import Paginator
from .filters import NewFilter

class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = ['-create_post']
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.datetime.utcnow()
        context['filter'] = NewFilter(self.request.GET, queryset=self.get_queryset())
        context['categories'] = Category.objects.all()
        return context

class NewDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'