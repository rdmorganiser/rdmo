from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User)

    def __str__(self):
        return str(self.user.username)

    def __unicode__(self):
        return unicode(self.__str__())

    class Meta:
        ordering = ("user",)
