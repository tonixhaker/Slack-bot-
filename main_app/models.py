from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=200)
    team_id = models.CharField(max_length=20)
    bot_user_id = models.CharField(max_length=20)
    bot_access_token = models.CharField(max_length=100)
    user = models.ForeignKey("ausers.User", on_delete=models.CASCADE)
    incoming_hook = models.CharField(max_length=400)
    channelid = models.CharField(max_length=100)


class Message(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=50)
    text = models.TextField()
