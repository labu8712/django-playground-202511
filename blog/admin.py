from django.contrib import admin

from blog.models import Article, Author, Tag


class ArticleInline(admin.StackedInline):
    model = Article
    extra = 1
    fields = ["title", "content", "is_published"]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "is_published",
        "created_at",
        "tag_count",
    ]
    list_filter = ["is_published", "created_at", "author"]
    search_fields = ["title", "content"]
    ordering = ["-created_at"]
    list_per_page = 20

    @admin.display(description="標籤數量")
    def tag_count(self, obj):
        return obj.tags.count()


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "created_at"]
    inlines = [ArticleInline]


admin.site.register(Tag)
