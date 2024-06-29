import re
from django.contrib.auth.decorators import login_required

from .filters import ResponseFilter
from .forms import ResponseForm, PostForm
from .models import Response, Post, Category

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .utils import response_not_in_user_post


class PostListView(ListView):
    model = Post
    ordering = '-pub_date'
    template_name = 'board/index.html'
    context_object_name = 'postlist'
    paginate_by = 5


class PostDetailView(DetailView):
    model = Post
    template_name = 'board/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('pk')
        post = Post.objects.get(pk=id)
        context['response_set'] = post.response_set.all().order_by('-pub_date')
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'board/post_create.html'
    form_class = PostForm

    # Field.initial/Field.disabled alt. solution
    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'board/post_update.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    # author verification
    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()

        context = {'post_id': post.pk}
        if post.user != self.request.user:
            return render(self.request, template_name='board/post_lock.html', context=context)

        return super(PostUpdateView, self).dispatch(request, *args, **kwargs)


class CategoryListView(PostListView):
    template_name = 'board/post_category.html'
    context_object_name = 'post_category'

    def get_queryset(self):
        # current category instance
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ResponseCreateView(LoginRequiredMixin, CreateView):
    model = Response
    form_class = ResponseForm
    template_name = 'board/response_create.html'
    context_object_name = 'response'

    def get_context_data(self, **kwargs):
        id = self.kwargs.get('pk')
        post = Post.objects.get(pk=id)
        context = super().get_context_data(**kwargs)
        context['post'] = post
        return context

    def form_valid(self, form):
        post_id = self.kwargs.get('pk')  # post.id from URL
        post = get_object_or_404(Post, pk=post_id)  # get Post object

        response = form.save(commit=False)
        response.post = post
        response.user = self.request.user
        response.save()

        return super().form_valid(form)


# for PersonalSearchListView
@login_required
def response_accept(request, pk):
    response = Response.objects.get(id=pk)
    if response_not_in_user_post(request, response):
        context = {'response_id': response.id}
        return render(request, template_name='board/response_lock.html', context=context)

    response.status = True
    response.save(update_fields=['status'])
    return redirect(request.META.get('HTTP_REFERER'))  # redirects to the previous page


# for PersonalSearchListView
@login_required
def response_decline(request, pk):
    response = Response.objects.get(id=pk)
    if response_not_in_user_post(request, response):
        context = {'response_id': response.id}
        return render(request, template_name='board/response_lock.html', context=context)

    response.status = False
    response.save(update_fields=['status'])
    return redirect(request.META.get('HTTP_REFERER'))  # redirects to the previous page


# for PersonalSearchListView
@login_required
def response_delete(request, pk):
    response = Response.objects.get(id=pk)
    if response_not_in_user_post(request, response):
        context = {'response_id': response.id}
        return render(request, template_name='board/response_lock.html', context=context)

    response.delete()
    return redirect(request.META.get('HTTP_REFERER'))  # redirects to the previous page


class PersonalSearchListView(LoginRequiredMixin, ListView):
    """
    Приватная страница с откликами на объявления пользователя,
    внутри которой он может фильтровать отклики по объявлениям,
    удалять их и принимать.
    """
    model = Response
    ordering = '-pub_date'
    template_name = 'board/personal.html'
    context_object_name = 'personal'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset().filter(post__user=self.request.user)
        self.queryset = ResponseFilter(self.request.GET, request=self.request, queryset=queryset)
        return self.queryset.qs  # return .qs, otherwise the filter doesn't work

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.queryset
        try:
            context['params'] = re.sub(r'page=\d*\&', '', context['filter'].data.urlencode())
        except AttributeError:
            context['params'] = None
        return context
