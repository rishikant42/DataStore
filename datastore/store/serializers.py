from rest_framework import serializers

from store.models import User, Form


class FormSerializer(serializers.ModelSerializer):
    user_uid = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='uid',
        required=True,
        write_only=True,
    )

    def validate(self, attrs):
        attrs['user_id'] = self.instance.user.id if self.instance else attrs.pop('user_uid').id
        return super().validate(attrs)

    class Meta:
        model = Form
        fields = (
            'uid', 'name', 'user_uid',
        )
