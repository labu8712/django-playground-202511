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

    def get_object(self, pk):
        return Article.objects.get(pk=pk)

    def get(self, request, pk):
        try:
            article = self.get_object(pk)
        except Article.DoesNotExist:
            return Response(
                {"detail": "找不到該文章"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            article = self.get_object(pk)
        except Article.DoesNotExist:
            return Response(
                {"detail": "找不到該文章"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            # 手動更新 Article 物件
            article.title = serializer.validated_data["title"]
            article.content = serializer.validated_data["content"]
            article.is_published = serializer.validated_data.get(
                "is_published", article.is_published
            )
            article.save()
            output_serializer = ArticleSerializer(article)
            return Response(output_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            article = self.get_object(pk)
        except Article.DoesNotExist:
            return Response(
                {"detail": "找不到該文章"}, status=status.HTTP_404_NOT_FOUND
            )
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
