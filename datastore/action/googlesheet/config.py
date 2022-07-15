from urllib.parse import urljoin

from django.conf import settings

ID = "gsheet"

CALLBACK_URL = "oauth2/callback/"

# Error Threshold
ERROR_COUNTER_THRESHOLD = 5

# Authorization configs
# Static configurations
AUTHORITY_URL = "https://accounts.google.com/o/"
AUTH_ENDPOINT = "oauth2/v2/auth"
TOKEN_ENDPOINT = "oauth2/v2/token"
scopes = [
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/spreadsheets.readwriteonly'
]

# Settings from environment variables
CLIENT_ID = settings.GOOGLE_SHEET_CLIENT_ID
CLIENT_SECRET = settings.GOOGLE_SHEET_CLIENT_SECRET

REDIRECT_URI = urljoin(settings.HOST_URL, f"api/{ID}/" + CALLBACK_URL)
