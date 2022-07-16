from django.db import models

from store.models import Form


class Action(models.Model):
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

    name = models.CharField(max_length=1024, null=True, blank=True)
    auth_type = models.CharField(
        max_length=50, choices=AUTH_TYPE_CHOICES, default=BASIC,
    )
    enabled = models.BooleanField(default=False)

    class Meta:
        db_table = 'action'


class ActionAuthConfig(models.Model):
    action = models.ForeignKey(Action, on_delete=models.CASCADE, null=True)
    form = models.OneToOneField(Form, on_delete=models.CASCADE, null=True)
    config = models.JSONField()
    is_valid = models.BooleanField(default=False)
    invalid_reason = models.TextField(blank=True)
    is_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'actionauthconfig'
