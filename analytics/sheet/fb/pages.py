import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, timezone
from facebook_business.adobjects.page import Page
from facebook_business.adobjects.pagepost import PagePost
from facebook_business.adobjects.user import User
from facebook_business.session import FacebookSession
from facebook_business.api import FacebookAdsApi


METRICS = ["post_engaged_users",        # Number of people who clicked anywhere in your post
    "post_negative_feedback",       # Number of times people took a negative action in your post (e.g. hid it)       
    "post_clicks",          # Number of times people clicked on anywhere in your posts without generating a story
    "post_impressions",         # Number of times your Page's post entered a person's screen.        
    "post_impressions_organic",         # Number of times your Page content was on screen through organic distribution
    "post_reactions_like_total",        # Total "like" reactions of a post
    "post_reactions_love_total",        # Total "love" reactions of a post
    "post_reactions_wow_total",         # Total "wow" reactions of a post
    "post_reactions_haha_total",        # Total "haha" reactions of a post
    "post_reactions_sorry_total",       # Total "sad" reactions of a post
    "post_reactions_anger_total"        # Total "anger" reactions of a post
]


def init_api(token=os.environ["USER_TOKEN"]):
    """Initialises and returns a default API object used to make API calls. 
    Default access token is the User Access Token."""
    return FacebookAdsApi.init(app_secret=os.environ["APP_SECRET"], access_token=token)

def get_api(access_token):
    """Returns API object with `access_token`."""
    session = FacebookSession(access_token=access_token)
    return FacebookAdsApi(session=session)

def get_pages_tokens():
    """Returns dictionary of Page Access Tokens for each page. Ensure theres a default API set using User Access Token before calling."""
    assert FacebookAdsApi.get_default_api() is not None, "Need to initialise a default API with User Access Token first."
    user = User("me")
    return {
        page_obj["name"]: page_obj["access_token"] for page_obj in user.get_accounts()
    }

def list_page_posts(page_api):
    page = Page("me", api=page_api)
    return page.get_posts()

def view_page_post(post_id, fields: list, page_api) -> dict:
    """Returns all the relevant `fields` of the page post specified by `page_id` as a dictionary."""
    page_post = PagePost(fbid=post_id, api=page_api)
    response = page_post.api_get(fields=fields)
    return response.export_value(response._data)

def count_comments(post_id, page_api):
    post = PagePost(fbid=post_id, api=page_api)
    response = post.get_comments()
    return len(response)

def page_post_insights(post_id, metrics: list, page_api):
    """Gets all page post insights specified in `metrics`."""
    params = {
        "metric": metrics
    }
    post = PagePost(fbid=post_id, api=page_api)
    return post.get_insights(params=params)

def generate_excel(excel_path=None):
    # Sets the default API using the User Access Token
    init_api()

    pages = get_pages_tokens()

    sheet_dict = {}
    for page_name, page_token in pages.items():
        # Get another API object configured with Page Access Token
        page_api = get_api(access_token=page_token)

        final_df = pd.DataFrame()
        for post in list_page_posts(page_api):
            post_id = post["id"]

            # Get relevant information from each post
            fields = [
                # PagePost.Field.id,
                PagePost.Field.created_time,
                PagePost.Field.message,
                PagePost.Field.permalink_url,
                PagePost.Field.shares
            ]

            json_dict = view_page_post(post["id"], fields, page_api)

            insight_dict = {
                # "id": json_dict["id"],
                "time_posted": datetime.strptime(json_dict["created_time"], "%Y-%m-%dT%H:%M:%S%z"),       # Convert UNIX timestamp string to datetime objects  
                "message": json_dict["message"][:50] if json_dict.get("message") else "",
                "link": json_dict["permalink_url"],
                "shares": json_dict["shares"]["count"] if json_dict.get("shares") else 0
            }  

            # Add comment count
            insight_dict = insight_dict | {"comments": count_comments(post_id, page_api)}

            # Combine insights data into dict
            insights = page_post_insights(post_id, METRICS, page_api)
            insight_dict = insight_dict | {insight["name"][5:]: insight["values"][0]["value"] for insight in insights}
            df = pd.DataFrame(insight_dict, index=[0])
            final_df = pd.concat([final_df, df], ignore_index=True)

        # Convert datetime objects to sgt time
        sgt = timezone(timedelta(hours=8), name="SGT")
        final_df["time_posted"] = final_df["time_posted"].dt.tz_convert(tz=sgt)
        final_df["time_posted"] = final_df["time_posted"].dt.strftime("%Y-%m-%d %H:%M:%S %Z")
        # final_df.to_excel(writer, sheet_name=page_name)
        page_name = page_name.strip()     # Remove trailing whitespace in name
        sheet_dict[page_name] = final_df

    if excel_path:
        with pd.ExcelWriter(excel_path) as writer:
            for page_name, sheet_df in sheet_dict.items():
                sheet_df.to_excel(writer, sheet_name=page_name)
    else:
        return sheet_dict
        