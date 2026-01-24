from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.viewsets import ModelViewSet

from blog.models import Article
from blog.serializers import ArticleSerializer


class ArticleViewSet(ModelViewSet):
    """文章 API ViewSet"""

    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "title"]
    filterset_fields = ["is_published", "author"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
