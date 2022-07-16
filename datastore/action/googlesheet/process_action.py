import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from action.models import GsheetAction
from store.models import Form


class GooglesheetAction:
    def __init__(self, form_id):
        self.form = Form.objects.get(id=form_id)
        self.gsheet = GsheetAction.objects.filter(
            auth_config__form_id=form_id
        ).first()
        self.creds, _ = google.auth.default()

    def create_sheet(self, title):
        try:
            service = build('sheets', 'v4', credentials=self.creds)
            spreadsheet = {
                'properties': {
                    'title': title
                }
            }
            spreadsheet = service.spreadsheets().create(
                body=spreadsheet,
                fields='spreadsheetId').execute()
            return spreadsheet.get('spreadsheetId')
        except HttpError as error:
            return error

    def update_sheet_values(self, spreadsheet_id, values):
        try:
            service = build('sheets', 'v4', credentials=self.creds)
            body = {
                'values': values
            }
            result = service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                body=body).execute()
            return result
        except HttpError as error:
            return error

    def create_or_update_sheet(self):
        if not self.gsheet:
            sheet_id = self.create_sheet(self.form.name)
            gsheet = GsheetAction.objects.creat(
                sheet_name=self.form.name,
                sheet_id=sheet_id,
                auth_config=self.form.actionauthconfig,
            )

        response = self.form.response_set.order_by('created_time').last()
        return self.update_sheet_values(gsheet.sheet_id, response.answers)

    def process_action(self):
        return self.create_or_update_sheet()
