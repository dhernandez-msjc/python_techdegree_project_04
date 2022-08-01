import csv
import datetime
from models.model import (session, Product)


def clean_product_id(product_id_string: str, available_options: list) -> int:
    pass


def clean_quantity(quantity_string: str) -> int:
    pass


def clean_price(price_string: str) -> int:
    pass


def clean_date(date_string: str) -> datetime.date:
    pass


def add_csv_data(csv_file_name: str) -> None:
    with open(csv_file_name) as csv_file:
        data = csv.reader(csv_file)

        for line in enumerate(data):
            product_exists_in_db = session.query(Product).filter(Product.product_name == line[0])
            print(line)
    pass


if __name__ == '__main__':
    add_csv_data('../models/data/inventory.csv')
