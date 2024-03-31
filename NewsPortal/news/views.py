from datetime import datetime

from django.views.generic import ListView, DetailView
from .models import Post


class PostList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context

    def get_queryset(self):
        return Post.objects.order_by("-date_in")


class PostDetail(DetailView):
    model = Post
    template_name = 'news_id.html'
    context_object_name = 'post'
