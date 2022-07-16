from rest_framework import serializers

from action.models import (
    Action, ActionAuthConfig,
)
from action.googlesheet.oauth2 import GsheetAuth
from store.models import Form


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = (
            'name', 'auth_type', 'enabled',
        )


class ActionAuthConfigSerializer(serializers.ModelSerializer):
    action_uid = serializers.SlugRelatedField(
        queryset=Action.objects.all(),
        slug_field='uid',
        required=True,
        write_only=True,
    )
    form_uid = serializers.SlugRelatedField(
        queryset=Form.objects.all(),
        slug_field='uid',
        required=True,
        write_only=True,
    )

    def validate(self, attrs):
        attrs['action'] = self.instance.action if self.instance else attrs.pop('action_uid')
        attrs['form'] = self.instance.form if self.instance else attrs.pop('form_uid')
        return super().validate(attrs)

    class Meta:
        model = ActionAuthConfig
        fields = (
            'action_uid', 'form_uid', 'config'
        )


class GsheetAuthConfigSerializer(ActionAuthConfigSerializer):
    authorization_url = serializers.SerializerMethodField()

    def get_authorization_url(self, obj):
        return GsheetAuth(obj).get_authorization_url(obj.action.id)

    def create(self, validated_data):
        validated_data['auth_config'] = {
            "state": validated_data.get('action').id,
            "is_authenticated": False,
            "access_token": None,
            "refresh_token": None,
            "access_token_expires_at": None,
        }
        return super().create(validated_data)

    class Meta:
        model = ActionAuthConfig
        fields = (
            'action_uid', 'form_uid', 'config', 'authorization_url',
        )
