from django.shortcuts import render


def hello_world(request):
    return render(request, "practices/hello.html")


def greeting(request):
    name = "Django"
    return render(request, "practices/greeting.html", {"name": name})
