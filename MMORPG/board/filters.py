from django_filters import FilterSet, ModelChoiceFilter
from .models import Post


def posts(request):
    if request is None:
        return Post.objects.none()

    user = request.user
    return user.post_set.all()


class ResponseFilter(FilterSet):
    title = ModelChoiceFilter(
        field_name='post__title',
        queryset=posts,
    )