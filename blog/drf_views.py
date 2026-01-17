from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Article
from blog.serializers import ArticleSerializer


class ArticleListAPIView(APIView):
    """文章列表 API"""

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            # 手動建立 Article 物件
            article = Article.objects.create(
                title=serializer.validated_data["title"],
                content=serializer.validated_data["content"],
                is_published=serializer.validated_data.get("is_published", False),
                created_by=request.user,
            )
            output_serializer = ArticleSerializer(article)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailAPIView(APIView):
    """文章詳情 API"""

    def get(self, request, pk):
        return Response({"message": f"取得文章 {pk}"})

    def put(self, request, pk):
        return Response({"message": f"更新文章 {pk}"})

    def delete(self, request, pk):
        return Response({"message": f"刪除文章 {pk}"}, status=204)
