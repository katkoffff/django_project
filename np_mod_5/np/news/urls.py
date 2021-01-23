from django.urls import path
from .views import NewsList, NewsDetail, NewsCreate, NewsUpdate, NewsDelete, NewsSearch


urlpatterns=[
    path('', NewsList.as_view(), name='news'),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('add/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('search/', NewsSearch.as_view(), name='news_search'),
]