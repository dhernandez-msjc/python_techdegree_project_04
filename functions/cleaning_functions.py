import csv
import datetime
from models.model import (session, Product)


def clean_product_id(product_id_string: str, available_options: list) -> int:
    pass


def clean_quantity(quantity_string: str) -> int:
    try:
        return_quantity = int(quantity_string)
    except ValueError:
        input('''
        \n************************** Quantity Error ****************************
        \rEnter an integer value for quantity.
        \rEx. 17
        \rPlease Try Again.
        \r**********************************************************************
        ''')
    else:
        return return_quantity


def clean_price(price_string: str) -> int:
    try:
        price_as_float = float(price_string.split('$')[1])
    except ValueError:
        input('''
        \n************************** Price Error ****************************
        \rEnter a value for price with dollar sign.
        \rEx. $19.76
        \rPlease Try Again.
        \r**********************************************************************
        ''')
    else:
        return int(price_as_float * 100)


def clean_date(date_string: str) -> datetime.date:
    try:
        month, day, year = date_string.split('/')
        month = int(month)
        day = int(day)
        year = int(year)
        return_date = datetime.date(year, month, day)
    except ValueError:
        input('''
        \n************************** Date Error ****************************
        \rEnter a valid date from the past.
        \rEx. 2/21/1986
        \rPlease Try Again.
        \r**********************************************************************
        ''')
    else:
        return return_date


def add_csv_data(csv_file_name: str) -> None:
    with open(csv_file_name) as csv_file:
        data = csv.reader(csv_file)
        header = next(data)

        for line in data:
            # check for repeats and isolate single product entry
            product_name, product_price, product_quantity, date_updated = line
            product_exists_in_db = session.query(Product).filter(Product.product_name == product_name)

            if product_exists_in_db is None:
                print('success')
                product_price = clean_price(product_price)
                product_quantity = clean_quantity(product_quantity)
                date_updated = clean_date(date_updated)

                new_product = Product(product_name=product_name, product_quantity=product_quantity,
                                      product_price=product_price, date_updated=date_updated)
                print(new_product)
                session.add(new_product)
            session.commit()


if __name__ == '__main__':
    pass
