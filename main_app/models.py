from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=200)
    team_id = models.CharField(max_length=20, unique=True)
    bot_user_id = models.CharField(max_length=20)
    bot_access_token = models.CharField(max_length=100)
    access_token = models.CharField(max_length=100)
    user = models.ManyToManyField("ausers.User")
    incoming_hook = models.CharField(max_length=400)
    channelid = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Message(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=50)
    user_name = models.CharField(max_length=100)
    text = models.TextField()


class Answer(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    text = models.TextField()
