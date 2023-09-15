from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
User = get_user_model()

class Intent(models.Model):
    intent_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.intent_name


class Example(models.Model):
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE, related_name='example', null=True, blank=True)
    example_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.example_name


class CustomAction(models.Model):
    action_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.action_name


class Responses(models.Model):
    action = models.CharField(max_length=255, null=True, blank=True)
    response_text = models.JSONField(default=list)

    def __str__(self):
        return self.action


class Story(models.Model):
    story = models.CharField(max_length=255, null=True, blank=True)
    steps = models.JSONField(default=list)

    def __str__(self):
        return self.story


class Entity(models.Model):
    entity = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.entity


class PolicyInformation(models.Model):
    policy_number = models.CharField(max_length=255, null=True, blank=True)
    policy_detail = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.policy_number


class Room(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True)


class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.timestamp}]'