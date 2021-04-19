from django_filters import FilterSet
from .models import Post

class NewFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'to_author': ['exact'],
            'header_post': ['icontains'],
            'create_post': ['lt'],
                }
