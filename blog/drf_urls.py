from django.urls import path

from blog import drf_views

app_name = "drf-blog"

urlpatterns = [
    path("articles", drf_views.article_list, name="article-list"),
    path("articles/<int:pk>", drf_views.article_detail, name="article-detail"),
]
