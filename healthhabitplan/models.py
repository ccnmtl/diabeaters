from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    label = models.CharField(max_length=256,default="")
    position = models.IntegerField(default=0)

    class Meta:
        ordering = ('position',)

    def __unicode__(self):
        return self.label

    def css(self):
        return slugify(self.label)

class Item(models.Model):
    label = models.CharField(max_length=256,default="")
    category = models.ForeignKey(Category)
    description = models.TextField(default="",blank=True)

    class Meta:
        order_with_respect_to = 'category'

    def __unicode__(self):
        return self.label

class Session(models.Model):
    user = models.ForeignKey(User)
    saved = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "session #%d for %s %s" % (self.number(),self.user.first_name, self.user.last_name)

    def number(self):
        r = Session.objects.filter(user=self.user,saved__lt=self.saved).count()
        return r + 1

class Magnet(models.Model):
    session = models.ForeignKey(Session)
    item = models.ForeignKey(Item)

    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)


