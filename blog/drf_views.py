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
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
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
