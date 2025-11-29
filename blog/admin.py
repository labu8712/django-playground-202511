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
    actions = ["publish_articles", "unpublish_articles"]

    @admin.display(description="標籤數量")
    def tag_count(self, obj):
        return obj.tags.count()

    @admin.action(description="發布選中的文章")
    def publish_articles(self, request, queryset):
        count = queryset.update(is_published=True)
        self.message_user(request, f"成功發布 {count} 篇文章")

    @admin.action(description="取消發布選中的文章")
    def unpublish_articles(self, request, queryset):
        count = queryset.update(is_published=False)
        self.message_user(request, f"成功取消發布 {count} 篇文章")


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "created_at", "has_published_articles"]
    inlines = [ArticleInline]

    @admin.display(description="有已發布的文章", boolean=True)
    def has_published_articles(self, obj):
        return obj.articles.filter(is_published=True).exists()


admin.site.register(Tag)
