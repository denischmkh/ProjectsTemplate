from django.db import models


class Post(models.Model):
    date = models.CharField()
    sender_id = models.BigIntegerField()
    chat_id = models.BigIntegerField()
    text = models.TextField(null=True)
    photo = models.CharField(null=True)
    comment_count = models.CharField(null=True)
    views = models.IntegerField(null=True)
    reactions = models.IntegerField(null=True)


class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField()
    chat_id = models.BigIntegerField()
    username = models.CharField(max_length=150, null=True, blank=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    image = models.CharField(null=True)

    is_bot = models.BooleanField(default=False)

    is_restricted = models.BooleanField(null=True, blank=True)
    is_fake = models.BooleanField(null=True, blank=True)
    is_scam = models.BooleanField(null=True, blank=True)
    is_premium = models.BooleanField(null=True, blank=True)

    scraped_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.CharField(null=True, blank=True)
    is_banned = models.BooleanField(default=False)

class ScheduledMessage(models.Model):
    chat_id = models.BigIntegerField()
    message_text = models.TextField()
    scheduled_time = models.DateTimeField()
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
