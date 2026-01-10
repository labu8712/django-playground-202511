from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView
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


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "blog/article_create.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        form.save_m2m()
        messages.success(self.request, f"文章「{self.object.title}」已成功建立。")
        return redirect(self.get_success_url())


@permission_required("blog.change_article", raise_exception=True)
def article_edit(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)
    if form.is_valid():
        article = form.save()
        messages.success(request, f"文章「{article.title}」已成功更新。")
        return redirect("blog:article_detail", article_id=article.id)

    return render(request, "blog/article_edit.html", {"form": form, "article": article})


@permission_required("blog.delete_article", raise_exception=True)
def article_delete(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == "POST":
        article.delete()
        messages.success(request, f"文章「{article.title}」已成功刪除。")
        return redirect("blog:article_list")

    return render(request, "blog/article_delete.html", {"article": article})


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
