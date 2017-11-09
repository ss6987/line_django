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

    def get_rooms(self):
        rooms = Room.objects.filter(user__in=[self])
        return rooms

    def get_room_names(self):
        rooms = Room.objects.filter(user__in=[self])
        room_names = []
        for room in rooms:
            room_names.append(room.get_name(self.username))
        return room_names


class Relationship(models.Model):
    follow = models.ForeignKey(User, related_name='follows')
    follower = models.ForeignKey(User, related_name='followers')

    class Meta:
        unique_together = ("follow", "follower")


class Room(models.Model):
    user = models.ManyToManyField(User, related_name="room")

    def get_name(self, username):
        room_name = ""
        users = self.user.all().filter(~models.Q(username=username))
        for user in users:
            room_name = room_name + user.username + ","
        return room_name[:len(room_name) - 1]

    def __str__(self):
        room_name = ""
        users = self.user.all()
        for user in users:
            room_name = room_name + user.username + ","
        return room_name[:len(room_name) - 1]


class Talk(models.Model):
    room = models.ForeignKey(Room, related_name="talk")
    user = models.ForeignKey(User, related_name="talk")
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(null=False, blank=False)
