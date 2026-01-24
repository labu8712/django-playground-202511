from typing import Annotated

from ninja import FilterLookup, FilterSchema, ModelSchema

from blog.models import Article


class ArticleIn(ModelSchema):
    class Meta:
        model = Article
        fields = ["title", "content", "is_published"]


class ArticleOut(ModelSchema):
    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "content",
            "is_published",
            "created_by",
            "author",
            "created_at",
            "updated_at",
        ]


class ArticleFilterSchema(FilterSchema):
    is_published: bool | None = None
    title__icontains: str | None = None
    search: Annotated[
        str | None, FilterLookup(["title__icontains", "content__icontains"])
    ] = None
