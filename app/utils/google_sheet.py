import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# READ FROM ENVIRONMENT VARIABLE
creds_dict = json.loads(os.environ.get("GOOGLE_CREDENTIALS"))

creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

sheet = client.open("Orders").sheet1


def save_order_to_sheet(order):
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
