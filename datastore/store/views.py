from rest_framework import viewsets, status
from rest_framework.response import Response

from store.models import (
    Form, Question,
)
from store.models import Response as FormResponse
from store.serializers import (
    FormSerializer, QuestionSerializer, ResponseSerializer,
)


class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    lookup_field = 'uid'


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = 'uid'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = FormResponse.objects.order_by('-created_time')
    serializer_class = ResponseSerializer
    lookup_field = 'uid'
