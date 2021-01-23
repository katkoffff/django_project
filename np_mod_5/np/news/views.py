#from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
import datetime
from django.core.paginator import Paginator
from .filters import NewsFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class NewsList(ListView):
    model = Post
    template_name = 'news_app/news.html'
    context_object_name = 'news'
    ordering = ['-create_post']
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.datetime.utcnow()
        #context['filter'] = NewFilter(self.request.GET, queryset=self.get_queryset())
        #context['categories'] = Category.objects.all()
        return context

class NewsDetail(DetailView):
    template_name = 'news_app/detail.html'
    context_object_name = 'news_detail'
    queryset = Post.objects.all()

class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    template_name = 'news_app/add.html'
    context_object_name = 'news_create'
    form_class = PostForm
    success_url = '/news/'


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'news_app/edit.html'
    context_object_name = 'news_update'
    form_class = PostForm
    success_url = '/news/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class NewsDelete(DeleteView):
    template_name = 'news_app/delete.html'
    context_object_name = 'news_delete'
    queryset = Post.objects.all()
    success_url = '/news/'

class NewsSearch(ListView):
    template_name = 'news_app/search.html'
    context_object_name = 'news_search'
    ordering = ['-create_post']
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.datetime.utcnow()
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context