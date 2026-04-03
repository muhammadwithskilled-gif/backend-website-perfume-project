# app/utils/google_sheet.py

import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google API scope
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# ------------------------------
# Load credentials from Environment Variable
# ------------------------------
creds_json = os.environ.get("GOOGLE_CREDENTIALS")  # <- This is the Render env variable
if not creds_json:
    raise Exception("GOOGLE_CREDENTIALS environment variable not set!")

creds_dict = json.loads(creds_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Open your Google Sheet
sheet = client.open("Orders").sheet1


def save_order_to_sheet(order):
    """
    Save order data into Google Sheet
    """
    sheet.append_row([
        order.get("product_name"),
        order.get("product_detail"),
        order.get("product_description"),
        order.get("delivery_time"),
        order.get("payment_method"),
        order.get("customer_name"),
        order.get("customer_address"),
        order.get("delivery_date"),
        order.get("status")
    ])
