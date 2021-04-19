from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import User, Post, Replay
from .forms import PostForm, UpdateForm, ReplayForm, ConfirmForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class NewsList(ListView):
    model = Post
    template_name = 'board/board.html'
    context_object_name = 'boards'
    paginate_by = 4
    ordering = ['-create']


class NewsDetail(DetailView):
    template_name = 'board/board_detail.html'
    context_object_name = 'boards_detail'
    queryset = Post.objects.all()


class NewsCreate(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    template_name = 'board/board_create.html'
    context_object_name = 'boards_create'
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        if not User.objects.filter(user=request.user).exists():
            User.objects.create(user=request.user)
        post = Post(author=User.objects.get(user=request.user))
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    success_url = '/board/'


class NewsUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login/'
    template_name = 'board/board_update.html'
    context_object_name = 'boards_update'
    form_class = UpdateForm
    success_url = '/board/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class NewsDelete(LoginRequiredMixin, DeleteView):
    login_url = '/accounts/login/'
    template_name = 'board/board_delete.html'
    context_object_name = 'boards_delete'
    queryset = Post.objects.all()
    success_url = '/board/'


class ReplayCreate(LoginRequiredMixin, CreateView):
    model = Replay
    login_url = '/accounts/login/'
    template_name = 'board/replay_create.html'
    context_object_name = 'replays_create'
    form_class = ReplayForm
    success_url = '/board/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Replay.objects.get(pk=id)

    def post(self, request, *args, **kwargs):
        if not User.objects.filter(user=request.user).exists():
            User.objects.create(user=request.user)
        replay = Replay(author=User.objects.get(user=request.user), post=Post.objects.get(pk=self.kwargs.get('pk')))
        form = self.form_class(request.POST, instance=replay)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)

class BoardReplay(ListView):
    model = Replay
    form_class = ConfirmForm
    template_name = 'board/board_replay.html'
    context_object_name = 'boards_replay'
    ordering = ['-create']
    paginate_by = 20
    queryset = Replay.objects.all()

@login_required(login_url = '/accounts/login/')
def subscribe(request, pk):
    replay = Replay.objects.get(id=pk)
    if request.POST.get('confirm'):
        replay.status = 'CF'
    elif request.POST.get('rejected'):
        replay.status = 'RJ'
    else:
        replay.status = 'WT'
    replay.save()
    return redirect('/board/board_replay/')



