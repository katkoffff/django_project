#from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author, Category, PostCategory, CategorySubscribers
import datetime
from django.core.paginator import Paginator
from .filters import NewsFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .tasks import hello


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

    def get(self, request):
        hello.delay()
        return HttpResponse('Hello!')


class NewsDetail(DetailView):
    template_name = 'news_app/detail.html'
    context_object_name = 'news_detail'
    queryset = Post.objects.all()

    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    #context['time_now'] = datetime.datetime.utcnow()
    #    #context['filter'] = NewFilter(self.request.GET, queryset=self.get_queryset())
    #    context['categories'] = PostCategory.objects.filter(to_post)
    #    return context

class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    template_name = 'news_app/add.html'
    context_object_name = 'news_create'
    form_class = PostForm
    success_url = '/news/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

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

class CategoryPost(DetailView):
    model = Category
    template_name = 'news_app/category.html'
    context_object_name = 'category'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        id = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        context['category_news'] = PostCategory.objects.filter(to_posts_id=id) #.values('to_categorys__name', 'to_posts_id', 'to_categorys_id', 'id')
        qs=context['category_news'].values('to_categorys__name', 'to_posts_id', 'to_categorys_id')
        context['user_is_anonymous'] = self.request.user.is_anonymous
        if not self.request.user.is_anonymous:
            lb=[]
            for p in qs:
                lb.append(CategorySubscribers.objects.filter(category__id=p['to_categorys_id'], user=self.request.user).exists())
            if all(lb):
                context['is_subscribe']=True
            else:
                context['is_subscribe']=False
        return context



@login_required
def subscribe_category(request):
    user = request.user
    id = request.META.get('HTTP_REFERER')[-11]
    qs = PostCategory.objects.filter(to_posts_id=id).values('to_categorys_id')
    for p in qs:
        category = Category.objects.get(id=p['to_categorys_id'])
        category.subscribers.add(user)
        try:
            send_mail(
                subject=f'subscribe',
                message=f'Вы были подписаны на категорию {category}',
                from_email='katkofff@yandex.ru',
                recipient_list=[f'{user.email}',]
            )
            print(f'send email to {user.email}')
        except Exception:
            print('spam')
    return redirect('/news/')

@login_required
def unsubscribe_category(request):
    user = request.user
    id = request.META.get('HTTP_REFERER')[-11]
    qs = PostCategory.objects.filter(to_posts_id=id).values('to_categorys_id')
    for p in qs:
        category = Category.objects.get(id=p['to_categorys_id'])
        category.subscribers.remove(user)
        try:
            send_mail(
                subject=f'unsubscribe ',
                message=f'Вы успешно отписались от темы {category}',
                from_email='katkofff@yandex.ru',
                recipient_list=[f'{user.email}', ]
            )
            print(f'send email to {user.email}')
        except Exception:
            print('spam')
    return redirect('/news/')

