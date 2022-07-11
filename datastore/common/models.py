from django.db import models


class AuthConfig(models.Model):
    BASIC = 'basic'
    TOKEN = 'token'
    HEADER = 'header'
    OAuth2 = 'OAuth2'

    AUTH_TYPE_CHOICES = (
        (BASIC, 'basic'),
        (TOKEN, 'token'),
        (HEADER, 'header'),
        (OAuth2, 'OAuth2'),
    )

    user_id = models.IntegerField(blank=False, null=True)
    action_id = models.CharField()
    config = models.JSONField()
    is_valid = models.BooleanField(default=False)
    invalid_reason = models.TextField(blank=True)
    is_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'authconfig'
