from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateFilter
from .models import Author
from django import forms


class PostFilter(FilterSet):
    search_title = CharFilter(
        field_name="title",
        label="Заголовок",
        lookup_expr="iregex"

    )

    search_author = ModelChoiceFilter(
        empty_label="Все авторы",
        field_name="author",
        label="Автор",
        queryset=Author.objects.all()

    )

    post_date = DateFilter(
        field_name="date_in",
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Дата",
        lookup_expr="date__gte"
    )
