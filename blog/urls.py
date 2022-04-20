from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path(r'',  views.index, name='index'),
    path(r'posts/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path(r'archives/<int:year>/<int:month>/', views.ArchiveView.as_view(), name='archive'),
    path(r'categories/<int:pk>/', views.CategoryView.as_view(), name='category'),
    path(r'tags/<int:pk>/', views.TagView.as_view(), name='tag'),
    path(r'search/', views.search, name='search'),
    path(r'create/',views.post_create,name='post_create')

]