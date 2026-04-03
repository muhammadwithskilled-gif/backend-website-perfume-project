import os
import json
from pathlib import Path

# Get current file location
BASE_DIR = Path(__file__).resolve().parent

# Go to backend root → then database folder
BASE_PATH = BASE_DIR.parent.parent / "database"

def get_all_products():
    products = []
    try:
        if not BASE_PATH.exists():
            print(f"❌ Database folder not found at: {BASE_PATH}")
            return []
            
        for folder in BASE_PATH.iterdir():
            if folder.is_dir():
                file_path = folder / "data.json"
                if file_path.exists():
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        products.append(data)
                        print(f"✅ Loaded: {data.get('name')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print(f"Total products: {len(products)}")
    return products


def get_product(product_id):
    for product in get_all_products():
        if str(product.get("id")) == str(product_id):
            return product
    return None