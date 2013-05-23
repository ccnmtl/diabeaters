from diabeaters.main.models import UserProfile
from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from django.core import management


class TrivialViewsTest(TestCase):
    def setUp(self):
        self.u = User.objects.create(username="testuser")
        self.u.set_password("foo")
        self.u.save()
        self.up = UserProfile.objects.create(user=self.u)
        self.c = Client()

    def tearDown(self):
        self.up.delete()
        self.u.delete()

    def test_root(self):
        response = self.c.get("/")
        self.assertEquals(response.status_code, 302)

    def test_smoketest(self):
        response = self.c.get("/smoketest/")
        self.assertEquals(response.status_code, 200)

    def test_about(self):
        response = self.c.get("/about/")
        self.assertEquals(response.status_code, 200)

    def test_home(self):
        response = self.c.get("/home/")
        self.assertEquals(response.status_code, 302)
        self.c.login(username="testuser", password="foo")
        response = self.c.get("/home/")
        self.assertEquals(response.status_code, 200)

    def test_session(self):
        management.call_command("import_diabeaters")
        response = self.c.get("/session-2/")
        self.assertEquals(response.status_code, 302)
        self.c.login(username="testuser", password="foo")
        response = self.c.get("/session-2/")
        self.assertEquals(response.status_code, 200)

        response = self.c.post("/session-2/", {'action': 'reset'})
        self.assertEquals(response.status_code, 302)

        response = self.c.post("/session-2/", {})
        self.assertEquals(response.status_code, 302)

        response = self.c.get("/edit/session-2/")
        self.assertEquals(response.status_code, 200)

        response = self.c.get("/instructor/session-2/")
        self.assertEquals(response.status_code, 200)

        self.u.is_staff = True
        self.u.save()

        response = self.c.get("/export/")
        self.assertEquals(response.status_code, 200)
