from rest_framework import serializers

from store.models import (
    User, Form, QuestionOption, Question, Response,
)
from store.tasks import process_form_response


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = (
            'uid', 'label', 'code',
        )


class QuestionSerializer(serializers.ModelSerializer):
    form_uid = serializers.SlugRelatedField(
        queryset=Form.objects.all(),
        slug_field='uid',
        required=True,
        write_only=True,
    )

    options = serializers.ListField(required=False, write_only=True)
    question_options = serializers.SerializerMethodField()

    def get_question_options(self, obj):
        return QuestionOptionSerializer(obj.options, many=True).data

    def validate(self, attrs):
        attrs['form_id'] = self.instance.form.id if self.instance else attrs.pop('form_uid').id
        return super().validate(attrs)

    def create(self, validated_data):
        q_options = validated_data.pop('options', None)
        if q_options:
            qos = QuestionOptionSerializer(data=q_options, many=True)
            if not qos.is_valid():
                raise serializers.ValidationError(qos.errors)
        instance = super().create(validated_data)
        if q_options:
            qos.save()
            instance.options.add(*qos.instance)
        return instance

    class Meta:
        model = Question
        fields = (
            'uid', 'form_uid', 'question_type', 'title', 'description',
            'keyword', 'is_mandatory', 'options', 'allow_none_option',
            'allow_all_option', 'lower_limit', 'upper_limit', 'allow_decimal',
            'date_format', 'time_format', 'question_options',
        )


class ResponseSerializer(serializers.ModelSerializer):
    form_uid = serializers.SlugRelatedField(
        queryset=Form.objects.all(),
        slug_field='uid',
        required=True,
        write_only=True,
    )
    user_uid = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='uid',
        required=True,
        write_only=True,
    )

    def validate(self, attrs):
        attrs['user_id'] = self.instance.user.id if self.instance else attrs.pop('user_uid').id
        attrs['form_id'] = self.instance.form.id if self.instance else attrs.pop('form_uid').id
        return super().validate(attrs)

    def create(self, validated_data):
        instance = super().create(validated_data)
        process_form_response.delay(instance.id)
        return instance

    class Meta:
        model = Response
        fields = (
            'uid', 'form_uid', 'user_uid', 'answers',
        )


class FormSerializer(serializers.ModelSerializer):
    user_uid = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='uid',
        required=True,
        write_only=True,
    )
    questions = serializers.SerializerMethodField()
    responses = serializers.SerializerMethodField()

    def get_questions(self, obj):
        return QuestionSerializer(obj.question_set.all(), many=True).data

    def get_responses(self, obj):
        return ResponseSerializer(obj.response_set.all(), many=True).data

    def validate(self, attrs):
        attrs['user_id'] = self.instance.user.id if self.instance else attrs.pop('user_uid').id
        return super().validate(attrs)

    class Meta:
        model = Form
        fields = (
            'uid', 'name', 'user_uid', 'questions', 'responses',
        )
