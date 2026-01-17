from django.urls import path

from blog import drf_views

app_name = "drf-blog"

urlpatterns = [
    path("articles", drf_views.ArticleListAPIView.as_view(), name="article-list"),
    path(
        "articles/<int:pk>",
        drf_views.ArticleDetailAPIView.as_view(),
        name="article-detail",
    ),
]
