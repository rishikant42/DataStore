import uuid

from django.db import models


class Form(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=220, null=False, blank=False)

    class Meta:
        db_table = 'form'


class QuestionOption(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    label = models.CharField(max_length=1024, null=False, blank=False)
    code = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        db_table = 'questionoption'



class Question(models.Model):
    SINGLE_CHOICE = 'SINGLE_CHOICE'
    MULTIPLE_CHOICE = 'MULTIPLE_CHOICE'
    TEXT = 'TEXT'
    NUMBER = 'NUMBER'
    LOCATION = 'LOCATION'
    DATE = 'DATE'
    TIME = 'TIME'
    NOTE = 'NOTE'

    TYPE_CHOICES = (
        (SINGLE_CHOICE, 'SINGLE_CHOICE'),
        (MULTIPLE_CHOICE, 'MULTIPLE_CHOICE'),
        (TEXT, 'TEXT'),
        (NUMBER, 'NUMBER'),
        (DATE, 'DATE'),
        (TIME, 'TIME'),
        (NOTE, 'NOTE'),
    )

    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    question_type = models.CharField(
        max_length=50, choices=TYPE_CHOICES, default=SINGLE_CHOICE,
    )
    title = models.CharField(max_length=1024, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    keyword = models.CharField(max_length=1024, null=False, blank=False)
    is_mandatory = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    # choice-type question sepcific columns
    options = models.ManyToManyField(QuestionOption)
    allow_none_option = models.BooleanField(default=False)
    allow_all_option = models.BooleanField(default=False)

    # number-type question specific columns
    lower_limit = models.FloatField(default=1.0)
    upper_limit = models.FloatField(default=100.0)
    allow_decimal = models.BooleanField(default=False)

    # date-type question specific columns
    date_format = models.CharField(max_length=50)

    # time-type question specific columns
    time_format = models.CharField(max_length=50)

    class Meta:
        db_table = 'question'


# class SingleChoiceQuestion(QuestionBase):
#     form = models.ForeignKey(Form, on_delete=models.CASCADE)
#     options = models.ManyToManyField(QuestionOption)
#     allow_none_option = models.BooleanField(default=False)
#
#
# class MultipleChoiceQuestion(QuestionBase):
#     form = models.ForeignKey(Form, on_delete=models.CASCADE)
#     options = models.ManyToManyField(QuestionOption)
#     allow_all_option = models.BooleanField(default=False)
