from django import forms

from blog.models import Author


class ArticleForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        required=True,
        label="標題",
        error_messages={
            "required": "標題不能空白",
            "max_length": "標題最多 %(limit_value)d 字元",
        },
    )
    content = forms.CharField(
        widget=forms.Textarea,
        required=True,
        label="內容",
        error_messages={
            "required": "內容不能空白",
        },
    )
    author = forms.ChoiceField(
        choices=[],
        required=False,
        label="作者",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["author"].choices = [("", "未指定")] + [
            (author.id, author.name) for author in Author.objects.all()
        ]
