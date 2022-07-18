from action.serializers import GsheetAuthConfigSerializer
from action.models import Action
from action.googlesheet.process_action import GooglesheetAction
from action.googlesheet.oauth2 import GsheetAuth


class ActionConfig:
    serializers_map = {
        'gsheet': GsheetAuthConfigSerializer,
    }
    action_map = {
        'gsheet': GooglesheetAction,
    }
    auth_map = {
        'gsheet': GsheetAuth,
    }

    def __init__(self, action_uid):
        self.action = Action.objects.get(uid=action_uid)
        return super().__init__()

    def get_serializer_class(self):
        return self.serializers_map(self.action.name)

    def get_action_class(self):
        return self.action_map(self.action.name)

    def get_auth_class(self, action_uid):
        return self.auth_map(self.action.name)
