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

        for index, line, in enumerate(data):
            # skip the headers
            if index == 0:
                continue

            # check for repeats and isolate single product entry
            product_name, product_price, product_quantity, date_updated = line
            product_exists_in_db = session.query(Product.__tablename__).filter(Product.product_name == product_name)

            if product_exists_in_db is None:
                product_price = clean_price(product_price)
                product_quantity = clean_quantity(product_quantity)
                date_updated = clean_date(date_updated)

                new_product = Product(product_name=product_name, product_quantity=product_quantity,
                                      product_price=product_price, date_updated=date_updated)
                print(new_product)
        #         session.add(new_product)
        # session.commit()


if __name__ == '__main__':
    add_csv_data('../models/data/inventory.csv')
