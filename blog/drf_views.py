from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from blog.models import Article
from blog.serializers import ArticleSerializer


class ArticleListAPIView(ListCreateAPIView):
    """文章列表 API"""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        """在建立物件時設定 created_by"""
        serializer.save(created_by=self.request.user)


class ArticleDetailAPIView(RetrieveUpdateDestroyAPIView):
    """文章詳情 API"""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
