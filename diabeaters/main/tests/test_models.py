from diabeaters.main.models import UserProfile
from django.test import TestCase
from django.contrib.auth.models import User


class UserProfileTest(TestCase):
    def setUp(self):
        self.u = User.objects.create(username="testuser")
        self.up = UserProfile.objects.create(user=self.u)

    def tearDown(self):
        self.up.delete()
        self.u.delete()

    def test_current_module(self):
        self.assertEquals(self.up.current_module(), None)
        self.up.current_location = "/"
        self.up.save()
        self.assertEquals(self.up.current_module(), None)
