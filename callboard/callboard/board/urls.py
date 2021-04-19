from django.urls import path
from .views import NewsList, NewsDetail, NewsCreate, NewsUpdate, NewsDelete, ReplayCreate, BoardReplay, subscribe


urlpatterns = [
    path('', NewsList.as_view(), name='boards'),
    path('<int:pk>', NewsDetail.as_view(), name='boards_detail'),
    path('board_create/', NewsCreate.as_view(), name='boards_create'),
    path('<int:pk>/board_update/', NewsUpdate.as_view(), name='boards_update'),
    path('<int:pk>/board_delete/', NewsDelete.as_view(), name='boards_delete'),
    path('<int:pk>/replay_create/', ReplayCreate.as_view(), name='replays_create'),
    path('board_replay/', BoardReplay.as_view(), name='boards_replay'),
    path('board_replay/subscribe/<int:pk>/', subscribe, name='subscribes'),
               ]