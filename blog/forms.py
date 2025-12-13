from django import forms


class ArticleForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        required=True,
        error_messages={
            "required": "標題不能空白",
            "max_length": "標題最多 %(limit_value)d 字元",
        },
    )
    content = forms.CharField(
        widget=forms.Textarea,
        required=True,
        error_messages={
            "required": "內容不能空白",
        },
    )
    author = forms.IntegerField(
        required=False,
    )
