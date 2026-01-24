import json
import os
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from playwright.sync_api import sync_playwright
from rest_framework import status
from rest_framework.test import APITestCase

from blog.models import Article

# Playwright 內部使用 async event loop, 需要允許 Django 在 async 環境中執行資料庫操作
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

User = get_user_model()


class LoginPageTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
        super().tearDownClass()

    def setUp(self):
        # 建立測試用使用者
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )

    def test_login_page_loads(self):
        """測試登入頁面能否正常載入"""
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/zh-hant/auth/login/")

        # 確認頁面標題包含「登入」
        assert "登入" in page.title()

        # 確認登入表單存在
        assert page.locator("form").count() > 0

        # 確認有使用者名稱和密碼輸入欄位
        assert page.locator("input[name='username']").count() == 1
        assert page.locator("input[name='password']").count() == 1

        # 確認有登入按鈕
        assert page.locator("form button[type='submit']").count() == 1

        page.close()

    def test_login_page_has_register_link(self):
        """測試登入頁面是否有註冊連結"""
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/zh-hant/auth/login/")

        # 確認有「立即註冊」連結
        register_link = page.locator("a", has_text="立即註冊")
        assert register_link.count() == 1

        page.close()

    def test_login_page_has_forgot_password_link(self):
        """測試登入頁面是否有忘記密碼連結"""
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/zh-hant/auth/login/")

        # 確認有「忘記密碼」連結
        forgot_link = page.locator("a", has_text="忘記密碼")
        assert forgot_link.count() == 1

        page.close()

    def test_successful_login(self):
        """測試成功登入的流程"""
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/zh-hant/auth/login/")

        # 填寫登入表單
        page.fill("input[name='username']", "testuser")
        page.fill("input[name='password']", "testpass123")

        # 點擊登入按鈕
        page.click("form button[type='submit']")

        # 等待頁面跳轉
        page.wait_for_url(f"{self.live_server_url}/zh-hant/blog/articles/")

        # 確認已登入, 導覽列應該顯示登出按鈕
        logout_button = page.locator("button", has_text=f"登出 ({self.user.username})")
        assert logout_button.count() == 1

        page.close()

    def test_failed_login(self):
        """測試登入失敗的情況"""
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/zh-hant/auth/login/")

        # 填寫錯誤的密碼
        page.fill("input[name='username']", "testuser")
        page.fill("input[name='password']", "wrongpassword")

        # 點擊登入按鈕
        page.click("form button[type='submit']")

        # 確認還在登入頁面
        assert "/auth/login/" in page.url

        # 確認有錯誤訊息
        error_message = page.locator("form .list-unstyled.text-danger")
        assert error_message.count() > 0

        assert (
            error_message.text_content().strip()  # type: ignore[reportOptionalMemberAccess]
            == "輸入正確的 使用者名稱 和密碼。請注意兩者皆區分大小寫。"
        )

        page.close()


class ArticleAPITests(APITestCase):
    """測試文章建立 API"""

    @classmethod
    def setUpTestData(cls):
        # 建立無權限使用者
        cls.user_without_permission = User.objects.create_user(
            username="normaluser",
            password="testpass123",
        )

        # 建立有權限的使用者
        cls.user_with_permission = User.objects.create_user(
            username="authorizeduser",
            password="testpass123",
        )

        # 賦予建立文章的權限
        add_article_permission = Permission.objects.get(codename="add_article")
        cls.user_with_permission.user_permissions.add(add_article_permission)

    def get_valid_payload(self):
        """取得有效的文章建立資料"""
        return {
            "title": "測試文章",
            "content": "這是測試內容",
            "is_published": False,
        }

    def test_create_article_unauthenticated(self):
        """未登入時建立文章應回傳 403"""
        response = self.client.post(
            "/api-drf/blog/articles",
            self.get_valid_payload(),
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_article_without_permission(self):
        """已登入但無權限時建立文章應回傳 403"""
        self.client.force_authenticate(user=self.user_without_permission)

        response = self.client.post(
            "/api-drf/blog/articles",
            self.get_valid_payload(),
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_article_with_permission(self):
        """已登入且有權限時應成功建立文章"""
        self.client.force_authenticate(user=self.user_with_permission)

        response = self.client.post(
            "/api-drf/blog/articles",
            self.get_valid_payload(),
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "測試文章"
        assert response.data["content"] == "這是測試內容"

        # 確認文章已建立在資料庫中
        assert Article.objects.filter(id=response.data["id"]).exists()

        # 確認 created_by 與其他欄位被正確設定
        article = Article.objects.get(id=response.data["id"])
        assert article.created_by == self.user_with_permission
        assert article.title == "測試文章"
        assert article.content == "這是測試內容"


class NinjaArticleAPITests(TestCase):
    """測試 Ninja 文章 API"""

    @classmethod
    def setUpTestData(cls):
        # 建立測試用使用者
        cls.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )

        # 建立測試文章
        cls.article = Article.objects.create(
            title="測試文章",
            content="這是測試內容",
            is_published=True,
            created_by=cls.user,
        )

    def test_get_article_success(self):
        """測試取得存在的文章"""
        response = self.client.get(f"/api-ninja/blog/articles/{self.article.id}")

        assert response.status_code == HTTPStatus.OK

        data = json.loads(response.content)
        assert data["id"] == self.article.id
        assert data["title"] == "測試文章"
        assert data["content"] == "這是測試內容"

    def test_get_article_not_found(self):
        """測試取得不存在的文章"""
        response = self.client.get("/api-ninja/blog/articles/99999")

        assert response.status_code == HTTPStatus.NOT_FOUND
