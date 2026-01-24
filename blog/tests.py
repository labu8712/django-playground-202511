import os

from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright

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
            error_message.text_content().strip()
            == "輸入正確的 使用者名稱 和密碼。請注意兩者皆區分大小寫。"
        )

        page.close()
