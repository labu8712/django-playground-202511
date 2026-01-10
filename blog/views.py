from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from blog.filters import ArticleFilter
from blog.forms import ArticleForm
from blog.models import Article


class ArticleListView(FilterView):
    queryset = Article.objects.select_related("author").prefetch_related("tags")
    filterset_class = ArticleFilter
    template_name = "blog/article_list.html"


class ArticleDetailView(DetailView):
    queryset = Article.objects.select_related("author").prefetch_related("tags")
    pk_url_kwarg = "article_id"


class ArticleCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "blog/article_create.html"
    permission_required = "blog.add_article"
    raise_exception = True
    success_message = "文章「%(title)s」已成功建立。"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "blog/article_edit.html"
    pk_url_kwarg = "article_id"
    permission_required = "blog.change_article"
    raise_exception = True
    success_message = "文章「%(title)s」已成功更新。"


class ArticleDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Article
    template_name = "blog/article_delete.html"
    pk_url_kwarg = "article_id"
    success_url = reverse_lazy("blog:article_list")
    permission_required = "blog.delete_article"
    raise_exception = True

    def get_success_message(self, cleaned_data):
        return f"文章「{self.object.title}」已成功刪除。"


@permission_required("blog.delete_article", raise_exception=True)
def article_bulk_delete(request):
    if request.method == "POST":
        article_ids = request.POST.getlist("article_ids")
        if article_ids:
            deleted_count, _ = Article.objects.filter(id__in=article_ids).delete()
            messages.success(request, f"已成功刪除 {deleted_count} 篇文章")
        else:
            messages.warning(request, "請先選取至少一個要刪除的文章")

    return redirect("blog:article_list")
