# Facebook Page Metrics Retriever
Simple Django Web Page that utilises the Facebook Graph API to retrieve Facebook page metrics data and compile into 
an excel sheet.

## Setup
1. Create an `.env` file using the `.env.example` template
2. Create a Meta Developer Account and create an application
3. Enable the following app permissions:
    * read_insights
    * pages_show_list
    * ads_management
    * pages_read_engagement
    * pages_manage_metadata
    * pages_read_user_content
    * pages_manage_engagement
4. Create a Google Developer Account