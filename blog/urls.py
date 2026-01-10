from django.urls import path

from blog import views

app_name = "blog"

urlpatterns = [
    path("articles/", views.article_list, name="article_list"),
    path("articles/create/", views.article_create, name="article_create"),
    path(
        "articles/<int:article_id>/",
        views.ArticleDetailView.as_view(),
        name="article_detail",
    ),
    path("articles/<int:article_id>/edit/", views.article_edit, name="article_edit"),
    path(
        "articles/<int:article_id>/delete/", views.article_delete, name="article_delete"
    ),
    path(
        "articles/bulk-delete/", views.article_bulk_delete, name="article_bulk_delete"
    ),
]
