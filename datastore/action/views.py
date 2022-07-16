from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView

from action.models import ActionAuthConfig
from action.action_config import ActionConfig


class ActionAuthConfigListView(CreateAPIView):
    queryset = ActionAuthConfig.objects.all()

    def get_serializer_class(self, obj):
        return ActionConfig().get_serializer_class(
            self.kwargs.get('action_uid')
        )


class ActionAuthConfigDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ActionAuthConfig.objects.all()
    lookup_field = 'uid'

    def get_serializer_class(self, obj):
        return ActionConfig().get_serializer_class(
            self.kwargs.get('action_uid')
        )
