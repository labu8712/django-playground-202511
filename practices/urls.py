from django.urls import path

from practices import views

urlpatterns = [
    path("hello/", views.hello_world, name="hello_world"),
]
