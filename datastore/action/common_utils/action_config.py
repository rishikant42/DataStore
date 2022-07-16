from action.serializers import GsheetAuthConfigSerializer
from action.models import Action
from action.googlesheet.process_action import GooglesheetAction


class ActionConfig:
    serializers_map = {
        'gsheet': GsheetAuthConfigSerializer,
    }
    action_map = {
        'gsheet': GooglesheetAction,
    }

    def get_serializer_class(self, action_uid):
        name = Action.objects.get(uid=action_uid).name
        return self.serializers_map(name)

    def get_action_class(self, action_uid):
        name = Action.objects.get(uid=action_uid).name
        return self.action_map(name)
