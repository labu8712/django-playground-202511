from django import forms

from blog.models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "author"]
        labels = {
            "title": "標題",
            "content": "內容",
            "author": "作者",
        }
        error_messages = {
            "title": {
                "required": "標題不能空白",
                "max_length": "標題最多 %(limit_value)d 字元",
            },
            "content": {
                "required": "內容不能空白",
            },
        }
        widgets = {
            "content": forms.Textarea(attrs={"rows": 10}),
        }
