from rest_framework.generics import (
    CreateAPIView, RetrieveUpdateDestroyAPIView,
)
from rest_framework.views import APIView
from django.shortcuts import render

from action.models import ActionAuthConfig
from action.common_utils.action_config import (
    Action, ActionConfig,
)


class ActionAuthConfigListView(CreateAPIView):
    queryset = ActionAuthConfig.objects.all()

    def get_serializer_class(self, obj):
        return ActionConfig(
            self.kwargs.get('action_uid')
        ).get_serializer_class()


class ActionAuthConfigDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ActionAuthConfig.objects.all()
    lookup_field = 'uid'

    def get_serializer_class(self, obj):
        return ActionConfig(
            self.kwargs.get('action_uid')
        ).get_serializer_class()


class OAuthCallback(APIView):
    def get(self, request, *args, **kwargs):
        action_id = request.query_params.get('state')
        action_obj  = Action.objects.filter(id=action_id).first()
        if not action_obj:
            return render(
                request, "oauth_callback.html", status=400
            )
        if not ActionConfig(action.uid).get_auth_class().callback_request(
            params.get("code"), params.get("state")
        ):
            return render(
                request, "oauth_callback.html", status=400
            )
        return render(request, "oauth_callback.html")
