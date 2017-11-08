from django.db import models
from django.contrib.auth.models import User as DjangoUser


class User(DjangoUser):
    class Meta:
        proxy = True

    def get_followers(self):
        relations = Relationship.objects.filter(follow=self)
        follower = []
        for relation in relations:
            follower.append(relation.follower)
        return follower


class Relationship(models.Model):
    follow = models.ForeignKey(User, related_name='follows')
    follower = models.ForeignKey(User, related_name='followers')

    class Meta:
        unique_together = ("follow","follower")