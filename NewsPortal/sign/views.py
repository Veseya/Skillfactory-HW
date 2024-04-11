from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView
from .models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserForm
from django.urls import reverse


from news.models import Author


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class UserProfileView(LoginRequiredMixin, UpdateView):
    form_class = UserForm
    model = User
    template_name = 'sign/profile.html'

    def get_object(self, **kwargs):
        id = self.request.user.pk
        return User.objects.get(pk=id)

    def get_success_url(self):
        return reverse('index')


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    Author.objects.create(user=user)
    return redirect('/')
