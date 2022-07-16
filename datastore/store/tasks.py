from celery import shared_task

from action.models import ActionAuthConfig
from action.common_utils.action_config import ActionConfig
from store.models import Response


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={'max_retries': 5}
)
def process_form_response(self, response_id):
    response = Response.objects.get(id=response_id)
    try:
        action = response.form.actionauthconfig.action
        resp_action = ActionConfig().get_action_class(action.uid)
        resp_action(response.form.id).process_action()
    except ActionAuthConfig.DoesNotExist:
        pass
    return True
