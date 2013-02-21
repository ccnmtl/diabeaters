from smoketest import SmokeTest
from django.contrib.auth.models import User


class DBConnectivity(SmokeTest):
    def test_retrieve(self):
        cnt = User.objects.all().count()
        self.assertTrue(cnt > 0)
