from abc import abstractmethod
from urllib import parse

from requests_oauthlib.oauth2_session import OAuth2Session


class OAuth2:
    def __init__(
        self,
        authority_url,
        auth_endpoint,
        token_end_point,
        client_id,
        client_secret,
        scopes,
        redirect_url,
    ):
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret
        self.SCOPES = scopes

        self.REDIRECT_URI = redirect_url
        self.TOKEN_ENDPOINT = parse.urljoin(authority_url, token_end_point)
        self.AUTH_BASE = parse.urljoin(authority_url, auth_endpoint)

    @property
    def session(self):
        return OAuth2Session(
            self.CLIENT_ID, scope=self.SCOPES, redirect_uri=self.REDIRECT_URI
        )

    def get_authorization_url(self, state):
        authorization_url, state = self.session.authorization_url(
            self.AUTH_BASE, state=state
        )
        return authorization_url

    def fetch_token(self, authorization_code):
        return self.session.fetch_token(
            self.TOKEN_ENDPOINT,
            client_secret=self.CLIENT_SECRET,
            code=authorization_code,
        )

    def handle_callback(self, authorization_code, auth_state, conn):
        if conn.auth_config.get("state") != auth_state:
            return False
        token_res = self.fetch_token(authorization_code)
        self.save_auth_config(token_res, conn)
        return True

    def refresh_token(self, conn):
        token_res = self.session.refresh_token(
            self.TOKEN_ENDPOINT,
            refresh_token=conn.auth_config["refresh_token"],
            client_id=self.CLIENT_ID,
            client_secret=self.CLIENT_SECRET,
        )
        self.save_auth_config(token_res, conn)

    @abstractmethod
    def save_auth_config(self, token_res, conn):
        raise NotImplementedError("override save_auth_config method to use")

    @abstractmethod
    def send_request(self, url, method, payload=None):
        raise NotImplementedError("override send_request method to use")
