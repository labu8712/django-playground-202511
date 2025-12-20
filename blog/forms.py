from django import forms

from blog.models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "author", "tags"]
        labels = {
            "title": "標題",
            "content": "內容",
            "author": "作者",
            "tags": "標籤",
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
            "tags": forms.CheckboxSelectMultiple(),
        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        if "測試" in title:
            error_message = "標題不能包含「測試」"
            raise forms.ValidationError(error_message)

        return title

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get("title")
        content = cleaned_data.get("content")

        if title == content:
            raise forms.ValidationError("內容不應與標題完全相等")

        return cleaned_data
