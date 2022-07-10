from rest_framework import viewsets

from store.models import Form
from store.serializers import FormSerializer


class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    lookup_field = 'uid'
