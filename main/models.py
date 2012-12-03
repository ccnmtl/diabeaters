from django.db import models
from django.contrib.auth.models import User
from pagetree.helpers import get_section_from_path, get_module


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    current_location = models.CharField(max_length=256, default="", blank=True)

    def current_module(self):
        if self.current_location == "":
            return None

        return get_module(get_section_from_path(self.current_location))
