from locust import HttpUser, task, between
from bs4 import BeautifulSoup
import logging

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.client.headers.update({
            "User-Agent": "locust-load-test-agent"
        })
        self.username = "testuser"
        self.password = "Test1234!"
        self.login_user()

    def login_user(self):
        response = self.client.get("/login")
        if response.status_code != 200:
            logging.error(f"Login page failed with status {response.status_code}")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        csrf_tag = soup.find("input", {"name": "csrf_token"})
        if not csrf_tag:
            logging.error("CSRF token not found on login page.")
            return

        csrf_token = csrf_tag.get("value")

        login_data = {
            "username": self.username,
            "password": self.password,
            "csrf_token": csrf_token
        }

        login_response = self.client.post("/login", data=login_data, allow_redirects=True)

        if "logout" in login_response.text.lower() or login_response.status_code == 200:
            logging.info(f"✅ Login successful for user: {self.username}")
        else:
            logging.error("❌ Login failed.")

    @task(5)
    def home(self):
        self.client.get("/")

    @task(2)
    def account(self):
        self.client.get("/account")

    @task(3)
    def create_page(self):
        self.client.get("/create")

    @task(2)
    def create_story(self):
        response = self.client.get("/create")
        soup = BeautifulSoup(response.text, "html.parser")
        csrf_tag = soup.find("input", {"name": "csrf_token"})
        if not csrf_tag:
            logging.warning("Missing CSRF on /create page.")
            return

        csrf_token = csrf_tag.get("value")

        data = {
            "title": "Locust Test Story",
            "content": "Dummy content",
            "csrf_token": csrf_token
        }
        self.client.post("/create", data=data)

    @task(2)
    def templates(self):
        self.client.get("/templates")

    @task(1)
    def help(self):
        self.client.get("/help")

    @task(2)
    def my_stories(self):
        self.client.get("/my_stories")
