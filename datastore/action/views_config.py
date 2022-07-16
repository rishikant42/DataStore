from action.serializers import GsheetAuthConfigSerializer


class ActionAuthConfigViewUtils:
    serializers_map = {
        # google sheet
        'a1b91721-4c29-48cf-b66a-4dae82851114': GsheetAuthConfigSerializer,
    }

    def get_serializer_class(self, action_id):
        return self.serializers_map(action_id)
