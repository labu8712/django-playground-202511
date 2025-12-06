from django.urls import path

from blog import views

urlpatterns = [
    path("articles/", views.article_list, name="article_list"),
    path("articles/<int:article_id>/", views.article_detail, name="article_detail"),
]
