from django.http import HttpResponse
from django.shortcuts import render


def hello_world(request):
    return render(request, "practices/hello.html")


def greeting(request):
    name = "Django"
    return render(request, "practices/greeting.html", {"name": name})


def search(request):
    keyword = request.GET.get("q", "")
    return HttpResponse(f"Keyword: {keyword}")


def product_list(request):
    category = request.GET.get("category", "all")
    sort = request.GET.get("sort", "newest")
    page = request.GET.get("page", "1")

    return HttpResponse(f"分類: {category}, 排序: {sort}, 頁數: {page}")


def filter_products(request):
    colors = request.GET.getlist("color")
    return HttpResponse(f"選擇的顏色: {', '.join(colors)}")


def hello_name(request, name):
    return HttpResponse(f"Hello, {name}!")
