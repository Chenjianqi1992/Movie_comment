from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:m_id>/', views.detail, name='detail'),
    path('<int:m_id>/comments', views.comments, name='comments'),
    #path('ajax1', views.ArticleListView.as_view(), name='ajax'),
    re_path(r'^ajax/search/$', views.ajax_search, name='ajax_search'),
    re_path(r'^search/$', views.comment_search, name='comment_search')
]
