import logging
from datetime import datetime, timedelta

import requests as requests
from common.auth.oauth2 import OAuth2
from action.googlesheet import config

logger = logging.getLogger(__name__)


class GsheetAuth(OAuth2):
    def __init__(self, auth_config=None):
        self.auth_config = auth_config
        super().__init__(
            authority_url=config.AUTHORITY_URL,
            auth_endpoint=config.AUTH_ENDPOINT,
            token_end_point=config.TOKEN_ENDPOINT,
            scopes=config.SCOPES,
            redirect_url=config.REDIRECT_URI,
            client_id=config.CLIENT_ID,
            client_secret=config.CLIENT_SECRET,
        )

    def save_auth_config(self, token_res, auth_config):
        if not token_res:
            logger.error(
                "Auth Request call failed for "
                f"user_id={self.auth_config.user_id} "
                f"integration={config.ID} "
                f"status_code={token_res.status_code} "
                f"response={token_res.text}"
            )
        else:
            auth_config.auth_config["access_token"] = token_res.get("access_token")
            auth_config.auth_config["refresh_token"] = token_res.get("refresh_token")
            auth_config.auth_config["access_token_expires_at"] = (
                datetime.utcnow() + timedelta(seconds=token_res.get("expires_in"))
            ).timestamp()
            auth_config.auth_config["is_authenticated"] = True
            auth_config.auth_config["state"] = None
            auth_config.save(update_fields=["auth_config"])

    def send_request(self, method, url, payload=None, params=None):
        if not self.auth_config:
            return {"message": "please create a valid auth_configection and try again!"}
        if (
            self.auth_config.auth_config["access_token_expires_at"]
            <= datetime.utcnow().timestamp()
        ):
            self.refresh_token(self.auth_config)
        response = requests.request(
            method,
            url,
            json=payload,
            params=params,
            headers={
                "Authorization": f'Bearer {self.auth_config.auth_config["access_token"]}'
            },
        )
        if not response:
            logger.error(
                "Request call failed for "
                f"user_id={self.auth_config.user_id} "
                f"integration={config.ID} "
                f"status_code={response.status_code} "
                f"method={method} url:{url} "
                f"response={response.text}"
            )
        return response

    def callback_request(self, authorization_code, auth_state):
        return self.handle_callback(authorization_code, auth_state, self.auth_config)
