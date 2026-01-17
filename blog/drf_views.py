from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET", "POST"])
def article_list(request):
    """文章列表 API"""
    if request.method == "GET":
        return Response({"message": "文章列表"})
    elif request.method == "POST":
        return Response({"message": "新增文章"}, status=201)


@api_view(["GET", "PUT", "DELETE"])
def article_detail(request, pk):
    """文章詳情 API"""
    if request.method == "GET":
        return Response({"message": f"取得文章 {pk}"})
    elif request.method == "PUT":
        return Response({"message": f"更新文章 {pk}"})
    elif request.method == "DELETE":
        return Response({"message": f"刪除文章 {pk}"}, status=204)
