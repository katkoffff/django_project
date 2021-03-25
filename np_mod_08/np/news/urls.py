from django.urls import path
from .views import NewsList, NewsDetail, NewsCreate, NewsUpdate, NewsDelete, NewsSearch, CategoryPost
from .views import subscribe_category, unsubscribe_category
from django.views.decorators.cache import cache_page


urlpatterns=[
    path('', cache_page(60*1)(NewsList.as_view()), name='news'),
    path('<int:pk>', cache_page(60*5)(NewsDetail.as_view()), name='news_detail'),
    path('add/', cache_page(60*5)(NewsCreate.as_view()), name='news_create'),
    path('<int:pk>/edit/', cache_page(60*5)(NewsUpdate.as_view()), name='news_update'),
    path('<int:pk>/delete/', cache_page(60*5)(NewsDelete.as_view()), name='news_delete'),
    path('search/', cache_page(60*5)(NewsSearch.as_view()), name='news_search'),
    path('<int:pk>/category/', cache_page(60*5)(CategoryPost.as_view()), name='category'),
    path('category/subscribe/', subscribe_category, name='subscribe'),
    path('category/unsubscribe/', unsubscribe_category, name='unsubscribe'),
]