from django.db import models
from django.contrib.auth.models import User
from pagetree.models import Hierarchy

def get_hierarchy():
    return Hierarchy.objects.get_or_create(name="main",defaults=dict(base_url="/"))[0]

def get_section_from_path(path):
    h = get_hierarchy()
    return h.get_section_from_path(path)

def get_module(section):
    """ get the top level module that the section is in"""
    if section.is_root:
        return None
    return section.get_ancestors()[1]


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    current_location = models.CharField(max_length=256,default="",blank=True)

    def current_module(self):
        if self.current_location == "":
            return None

        return get_module(get_section_from_path(self.current_location))
  
