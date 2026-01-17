from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from blog.models import Article
from blog.serializers import ArticleSerializer


class ArticleListAPIView(GenericAPIView):
    """文章列表 API"""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request):
        articles = self.get_queryset()
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailAPIView(GenericAPIView):
    """文章詳情 API"""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, pk):
        article = self.get_object()
        serializer = self.get_serializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        article = self.get_object()
        serializer = self.get_serializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = self.get_object()
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
