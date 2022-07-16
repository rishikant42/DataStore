from action.serializers import GsheetAuthConfigSerializer
from action.models import Action


class ActionConfig:
    serializers_map = {
        'gsheet': GsheetAuthConfigSerializer,
    }

    def get_serializer_class(self, action_uid):
        name = Action.objects.get(uid=action_uid).name
        return self.serializers_map(name)
