from django.conf import settings
from django.db import models
from django.templatetags.static import static

from blog.validators import validate_image_size


class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    cover_image = models.ImageField(
        upload_to="articles/covers/",
        blank=True,
        null=True,
        validators=[validate_image_size],
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

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

    def __str__(self):
        return self.title

    def get_cover_image_url(self):
        if self.cover_image:
            return self.cover_image.url

        return static("blog/images/default-cover.jpg")
