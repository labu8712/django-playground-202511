from rest_framework.response import Response
from rest_framework.views import APIView


class ArticleListAPIView(APIView):
    """文章列表 API"""

    def get(self, request):
        return Response({"message": "文章列表"})

    def post(self, request):
        return Response({"message": "新增文章"}, status=201)


class ArticleDetailAPIView(APIView):
    """文章詳情 API"""

    def get(self, request, pk):
        return Response({"message": f"取得文章 {pk}"})

    def put(self, request, pk):
        return Response({"message": f"更新文章 {pk}"})

    def delete(self, request, pk):
        return Response({"message": f"刪除文章 {pk}"}, status=204)
