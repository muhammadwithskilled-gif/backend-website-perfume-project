# # app/utils/google_sheet.py

# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# # Google API scope
# scope = [
#     "https://spreadsheets.google.com/feeds",
#     "https://www.googleapis.com/auth/drive"
# ]

# # Load credentials
# creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
# client = gspread.authorize(creds)

# # Open your sheet
# sheet = client.open("Orders").sheet1


# def save_order_to_sheet(order):
#     """
#     Save order data into Google Sheet
#     """

#     sheet.append_row([
#         order.get("product_name"),
#         order.get("product_detail"),
#         order.get("product_description"),
#         order.get("delivery_time"),
#         order.get("payment_method"),
#         order.get("customer_name"),
#         order.get("customer_address"),
#         order.get("delivery_date"),
#         order.get("status")
#     ])
