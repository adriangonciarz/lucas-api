import base64
import csv
import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

csv_filepath = os.getenv("CSV_FILEPATH")
db_connection_string = os.getenv("MONGODB_URI")

client = MongoClient(db_connection_string)

ALL_PRODUCTS = []


def read_csv_file():
    with open(csv_filepath, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row['Title']:
                ALL_PRODUCTS.append({
                    'name': row['Title'],
                    'brand': row['Vendor'],
                    'price': row['Variant Price'],
                    'main_image': row['Image Src'],
                    'description': base64.b64encode(row['Body (HTML)'].encode('utf-8'))
                })
    print(ALL_PRODUCTS)


def insert_to_database():
    db = client['products']
    products = db['products']
    products.insert_many(ALL_PRODUCTS)


if __name__ == '__main__':
    read_csv_file()
    insert_to_database()
