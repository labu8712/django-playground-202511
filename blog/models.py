from django.conf import settings
from django.db import models
from django.templatetags.static import static
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from blog.validators import (
    validate_image_dimensions,
    validate_image_extension,
    validate_image_size,
)


class Author(models.Model):
    name = models.CharField(_("姓名"), max_length=100)
    email = models.EmailField(_("電子郵件"), unique=True)
    bio = models.TextField(_("個人簡介"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("author")
        verbose_name_plural = _("authors")

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(_("名稱"), max_length=50, unique=True)

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(_("標題"), max_length=200)
    content = models.TextField(_("內容"))
    cover_image = models.ImageField(
        _("封面圖片"),
        upload_to="articles/covers/",
        blank=True,
        null=True,
        validators=[
            validate_image_size,
            validate_image_extension,
            validate_image_dimensions,
        ],
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(_("是否發布"), default=False)

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="articles",
        null=True,
        blank=True,
    )

    tags = models.ManyToManyField(
        Tag,
        related_name="articles",
        blank=True,
    )

    class Meta:
        verbose_name = _("article")
        verbose_name_plural = _("articles")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:article_detail", kwargs={"article_id": self.pk})

    def get_cover_image_url(self):
        if self.cover_image:
            return self.cover_image.url

        return static("blog/images/default-cover.jpg")
