from .views import PostListView, PostDetailView, CategoryListView, PostCreateView, PostUpdateView, \
    ResponseCreateView, PersonalSearchListView, response_delete, response_accept, response_decline

from django.urls import path

urlpatterns = [
    path('', PostListView.as_view(),name='board'),
    path('<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('category/<int:pk>', CategoryListView.as_view(), name='post_category'),
    path('post/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/response/', ResponseCreateView.as_view(), name='response_create'),
    path('personal/', PersonalSearchListView.as_view(), name='personal_search'),
    path('<int:pk>/delete/', response_delete, name='response_delete'),
    path('<int:pk>/accept/', response_accept, name='response_accept'),
    path('<int:pk>/decline/', response_decline, name='response_decline'),
]