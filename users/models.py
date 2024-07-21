import os.path

from django.db import models
from django.contrib.auth.models import User
from PIL import Image

from django.db import models
from django.contrib.auth.models import User

class Clan(models.Model):
    name=models.CharField(max_length=72,unique=True)
    motto=models.CharField(max_length=256,unique=True)
    description=models.TextField(null=True,blank=True)
    leader=models.OneToOneField(User,on_delete=models.SET_NULL,null=True,blank=True)
    creation_date=models.DateField(auto_now_add=True)
    level = models.PositiveIntegerField(default=1)
    experience = models.PositiveIntegerField(default=0)
    emblem=models.ImageField(upload_to="emblems/",null=True,blank=True,default="default_emblem.jpg")

    def __str__(self):
        return self.name

class Player(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    nickname=models.CharField(max_length=60,unique=True)
    bio=models.CharField(max_length=256,null=True)
    credits=models.FloatField(default=0.0)
    level=models.PositiveIntegerField(default=1)
    experience=models.PositiveIntegerField(default=0)
    avatar=models.ImageField(upload_to="avatar/",null=True,blank=True,default="default.jpg")
    clan=models.OneToOneField(Clan,on_delete=models.CASCADE,null=True,blank=True)
    friends=models.ManyToManyField("self",symmetrical=True,blank=True)

    def __str__(self):
        return self.nickname

    def add_friend(self,friend):
        self.friends.add(friend)
        friend.friends.add(self)



class FriendRequest(models.Model):
    sender = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='sent_friend_requests')
    receiver = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='received_friend_requests')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"

class ClanRequest(models.Model):
    sender = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='sent_clan_requests')
    receiver = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='received_clan_requests')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver} (Clan)"