from django.contrib.auth import get_user_model
from django.db import models
import json


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
    response_text = models.JSONField(default=list, null=True, blank=True)
    another_list = models.TextField(null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     response = json.dump(self.another_list)
    #     self.response_text = response.text
    #     super().save(*args, **kwargs)
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
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True, related_name='room_user')


class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.timestamp}]'


class Contractor(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class Definition(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    details = models.TextField(null=True, blank=True)


class InsuranceType(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    keywords = models.JSONField(default=list)


class Form(models.Model):
    form_name = models.CharField(max_length=255, null=True, blank=True)
    slots = models.JSONField(default=list)


class Slot(models.Model):
    slot_name = models.CharField(max_length=255, null=True, blank=True)
    mappings = models.JSONField(default=list)


class Rule(models.Model):
    rule_name = models.CharField(max_length=255, null=True, blank=True)
    steps = models.JSONField(default=list)


class ConstractorInsuranceType(models.Model):
    insurance_type = models.CharField(max_length=255, null=True, blank=True)
    insurance_description = models.TextField(null=True, blank=True)


class InsuranceCost(models.Model):
    insurance_type = models.ForeignKey(ConstractorInsuranceType, related_name='insurance_cost',
                                       null=True, blank=True, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, null=True, blank=True)
    cost = models.CharField(max_length=255, null=True, blank=True)
    quotes = models.TextField(null=True, blank=True)
    legal_requirements = models.TextField(null=True, blank=True)


class CoverageOptions(models.Model):
    insurance_type = models.ForeignKey(ConstractorInsuranceType, related_name='insurance_coverage',
                                       null=True, blank=True, on_delete=models.CASCADE)
    options = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
