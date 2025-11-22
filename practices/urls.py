from django.urls import path

from practices import views

urlpatterns = [
    path("hello/", views.hello_world, name="hello_world"),
    path("greeting/", views.greeting, name="greeting"),
    path("search/", views.search, name="search"),
    path("products/", views.product_list, name="product_list"),
    path("products/filter/", views.filter_products, name="product_filter"),
    path("hello/<str:name>/", views.hello_name, name="hello_name"),
]
