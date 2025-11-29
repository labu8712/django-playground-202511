from django.contrib import admin

from blog.models import Article, Author, Tag


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "created_at"]


admin.site.register(Article)
admin.site.register(Tag)
