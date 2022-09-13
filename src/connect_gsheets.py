from apiclient import discovery
from dotenv import dotenv_values
from google.oauth2.service_account import Credentials

ENV = dotenv_values('.env')


def create_service():
    SECRET_FILE = ENV['GTOKEN']
    scopes = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/spreadsheets',
    ]
    credentials = Credentials.from_service_account_file(
        SECRET_FILE, scopes=scopes
    )
    service = discovery.build('sheets', 'v4', credentials=credentials)
    return service


def export_dataset(gsheet_id, dataframe):
    service = create_service()
    service_sheet = service.spreadsheets()

    values = dataframe.values.tolist()
    body = {'values': values}
    range_name = 'ExpectativasMercadoAnuais!A2'

    result = (
        service_sheet.values()
        .update(
            spreadsheetId=gsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body,
        )
        .execute()
    )
