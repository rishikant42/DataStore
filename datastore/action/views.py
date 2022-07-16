import json
from uuid import uuid4

from excel365 import config
from excel365.handlers import api_handler
from excel365.handlers.auth_handler import AuthHandler
from excel365.models import Connection
from excel365.serializers.connection import Excel365ConnectionSerializer
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response


class Excel365Connections(CreateAPIView):
    def post(self, request, *args, **kwargs):
        connection_data = request.data
        user_id = connection_data.get("user_id")
        user_email = connection_data.get("user_email")
        state = json.dumps({"user_id": user_id, "session": str(uuid4())})
        conn = Excel365ConnectionSerializer(
            data={
                "org_id": connection_data.get("org_id"),
                "user_id": user_id,
                "user_email": user_email,
                "sync_enabled": connection_data.get("sync_enabled"),
                "auth_config": {
                    "state": state,
                    "is_authenticated": False,
                    "access_token": None,
                    "refresh_token": None,
                    "access_token_expires_at": None,
                },
            }
        )
        if conn.is_valid():
            model_obj = Connection.objects.filter(
                user_id=user_id, integration_id=config.ID
            ).first()
            if model_obj:
                model_obj.auth_config["state"] = state
                model_obj.save(update_fields=["auth_config"])
            else:
                model_obj = conn.save()
        else:
            return Response(conn.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {
                "url": AuthHandler(model_obj).get_authorization_url(
                    model_obj.auth_config.get("state")
                )
            },
            status=status.HTTP_200_OK,
        )


class Excel365ConnectionDetails(RetrieveUpdateDestroyAPIView):
    lookup_field = "user_id"
    serializer_class = Excel365ConnectionSerializer
    queryset = Connection.objects.filter(integration_id=config.ID)

    def patch(self, request, *args, **kwargs):
        conn = self.get_object()
        request_data = request.data
        if not conn.auth_config["is_authenticated"]:
            return Response(
                {"is_valid": False, "message": "connection is not authenticated"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        is_valid, reason = api_handler.ValidateAPIs(conn).is_valid_connection()
        conn.is_valid = is_valid
        conn.enabled = is_valid
        conn.sync_enabled = request_data.get("sync_enabled", True)
        conn.invalid_reason = reason
        conn.disabled_reason = reason
        conn.save(
            update_fields=["is_valid", "sync_enabled", "invalid_reason", "enabled"]
        )
        return Response({"is_valid": conn.is_valid, "sync_enabled": conn.sync_enabled})
