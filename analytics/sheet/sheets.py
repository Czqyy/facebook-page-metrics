import os
from fb.pages import generate_excel
import pandas as pd
from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly", "https://www.googleapis.com/auth/spreadsheets"]


def get_creds():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        return creds
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
        return creds


def update_sheet(spreadsheetId, sheet_dict):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = get_creds()

    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        for page_name, df in sheet_dict.items():
            # Convert int64 columns to int
            for col in df.select_dtypes(include=['int64']).columns:
                df[col] = df[col].astype('object')

            # Convert dataframe to nested list
            values = []
            values.append(df.columns.tolist())
            for i in range(len(df)):
                series = df.iloc[i]
                values.append(series.tolist())

            body = {"values": values}
            sheet.values().update(
                spreadsheetId=spreadsheetId,
                range=f"{page_name}!A:Q",
                valueInputOption="USER_ENTERED", 
                # valueInputOption="RAW",        
                body=body
            ).execute()
        service.close()
        print("Sheets updated.")

    # try:
    #     service = build("sheets", "v4", credentials=creds)

    #     # Call the Sheets API
    #     sheet = service.spreadsheets()
    #     result = (
    #         sheet.values()
    #         .get(spreadsheetId=SPREADSHEET_ID, cell_range=SAMPLE_RANGE_NAME)
    #         .execute()
    #     )
    #     values = result.get("values", [])

    #     if not values:
    #         print("No data found.")
    #         return

    #     print(values)
    except HttpError as err:
        print(err)
        service.close()

# def create(title):
#     """
#     Creates the Sheet the user has access to.
#     Load pre-authorized user credentials from the environment.
#     TODO(developer) - See https://developers.google.com/identity
#     for guides on implementing OAuth2 for the application.
#     """
#     creds, _ = google.auth.default()
#     # pylint: disable=maybe-no-member
#     try:
#         service = build("sheets", "v4", credentials=creds)
#         spreadsheet = {"properties": {"title": title}}
#         spreadsheet = (
#             service.spreadsheets()
#             .create(body=spreadsheet, fields="spreadsheetId")
#             .execute()
#         )
#         print(f"Spreadsheet ID: {(spreadsheet.get('spreadsheetId'))}")
#         return spreadsheet.get("spreadsheetId")
#     except HttpError as error:
#         print(f"An error occurred: {error}")
#         return error


if __name__ == "__main__":
    sheet_dict = generate_excel()
    update_sheet(os.environ["SPREADSHEET_ID"], sheet_dict)