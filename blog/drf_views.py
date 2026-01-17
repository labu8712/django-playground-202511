from rest_framework.viewsets import ModelViewSet

from blog.models import Article
from blog.serializers import ArticleSerializer


class ArticleViewSet(ModelViewSet):
    """文章 API ViewSet"""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
