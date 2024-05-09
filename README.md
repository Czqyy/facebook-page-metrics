# Facebook Page Metrics Retriever
Simple Django Web Page that utilises the Facebook Graph API to retrieve Facebook page metrics data and compile into 
an excel sheet.

## Setup
1. Create a Meta Developer Account and create an application
2. Enable the following app permissions:
    * read_insights
    * pages_show_list
    * ads_management
    * pages_read_engagement
    * pages_manage_metadata
    * pages_read_user_content
    * pages_manage_engagement
3. Create a Google Cloud Project and enable the Google Sheets API (Follow this [guide](https://developers.google.com/sheets/api/quickstart/python))
4. Create an `.env` file using the `.env.example` template.
5. Install packages with `pip install -r requirements.txt`
6. Run Django App with `python manage.py runserver`
