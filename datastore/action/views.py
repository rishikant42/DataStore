from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView

from action.models import ActionAuthConfig
from action.views_config import ActionAuthConfigViewUtils


class ActionAuthConfigListView(CreateAPIView):
    queryset = ActionAuthConfig.objects.all()

    def get_serializer_class(self, obj):
        return ActionAuthConfigViewUtils().get_serializer_class(
            self.kwargs.get('action_uid')
        )


class ActionAuthConfigDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ActionAuthConfig.objects.all()
    lookup_field = 'uid'

    def get_serializer_class(self, obj):
        return ActionAuthConfigViewUtils().get_serializer_class(
            self.kwargs.get('action_uid')
        )
