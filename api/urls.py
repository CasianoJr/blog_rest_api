from . import views
from django.urls import path

urlpatterns = [
    path('', views.intro, name="introduction"),
    path('whoami/', views.WhoAmIView.as_view(), name="whoami"),
    path('articles/', views.ArticleListCreateView.as_view(),
         name='article-list-create'),
    path('article/<slug>/detail/', views.ArticleEditUpdateDeleteView.as_view(),
         name='article-detail'),
    path('article/<slug>/comment/', views.CommentCreateView.as_view(),
         name='comment-create'),
    path('comment/<slug>/detail/', views.CommentEditUpdateDeleteView.as_view(),
         name='comment-detail'),
    path('article/<slug>/image/', views.ImageCreateView.as_view(),
         name='image-create'),
    path('article/<slug>/like/', views.post_like_view, name='comment-create'),
    path('image/<slug>/detail/', views.ImageEditUpdateDeleteView.as_view(),
         name='image-detail'),
    path('comment/<slug>/nested_comment/', views.NestedCommentCreateView.as_view(),
         name='nested-comment-create'),
    path('nested_comment/<slug>/detail/',
         views.NestedCommentEditUpdateDeleteView, name='nested-comment-detail'),
    path('categories/', views.CategoryListCreateView.as_view(), name='category'),
]
