import datetime
import time
from enum import Enum
from models.menu import (MenuItem, Menu)
from models.model import (session, Product)
import functions.cleaning_functions as clean


class AppSetting(Enum):
    GAP_LENGTH = 7
    BORDER_SYMBOL = '>'


class ProductDisplay(Enum):
    ID = Product.product_id
    NAME = Product.product_name
    PRICE = Product.product_price
    QUANTITY = Product.product_quantity
    DATE = Product.date_updated
    BORDER_SYMBOL = '~'


class NewProduct(MenuItem):
    """
    Functor for adding a new product to the database.
    """

    def execute(self) -> None:
        product_name = input('Enter the product name: ')
        product_price = _get_valid_price()
        product_quantity = _get_valid_quantity()
        date_updated = _get_valid_date()

        new_product = Product(product_name=product_name, product_price=product_price,
                              product_quantity=product_quantity, date_updated=date_updated)
        session.add(new_product)
        session.commit()
        print('New product has been added.')
        time.sleep(1.5)


class ViewProducts(MenuItem):
    """
    Functor for viewing all available products by
    product ID.
    """

    def execute(self) -> None:
        products = session.query(Product)
        digit_length = _determine_digit_length()
        border_length = _calculate_border_length()
        border = AppSetting.BORDER_SYMBOL.value * border_length

        print(f'\n{border}')
        print(f'\r{"Inventory List": ^{border_length}}')
        print(f'{border}')
        for product in products:
            product_name_split = product.product_name.split(' - ')
            name = product_name_split[0]
            description = product_name_split[1] if len(product_name_split) > 1 else None
            print(f'{product.product_id: >{digit_length}}) '
                  f'{name:{_get_longest_product_name_length()}}'
                  f' {" - " + description if description is not None else ""}')
        print(border)


class ViewProductById(MenuItem):

    def execute(self) -> None:
        product_view = ViewProducts()
        product_view.execute()

        selected_product_id = _get_valid_id()
        product = session.query(Product).filter(Product.product_id == selected_product_id).first()
        displays = [ProductDisplay.NAME, ProductDisplay.PRICE, ProductDisplay.QUANTITY, ProductDisplay.DATE]
        # Menu.clear_console()
        _display_product(f'Product ID: {product.product_id}', product, displays)


# TODO add sub menu for editing product


class EditProduct(MenuItem):
    pass


class DeleteProduct(MenuItem):
    pass


class ProductAnalysis(MenuItem):
    """
    Functor for displaying product analysis.
    """

    def execute(self) -> None:
        most_expensive_product = session.query(Product).order_by(Product.product_price.desc()).first()
        least_expensive_product = session.query(Product).order_by(Product.product_price).first()

        most_common_product = session.query(Product).order_by(Product.product_quantity.desc()).first()
        least_common_product = session.query(Product).order_by(Product.product_quantity).first()

        average_product_price = _get_average_product_price()

        display_properties = [ProductDisplay.NAME, ProductDisplay.PRICE, ProductDisplay.QUANTITY]
        # Menu.clear_console()
        print(f'{"INVENTORY ANALYSIS": ^{_calculate_border_length()}}')
        _display_product('Most expensive product', most_expensive_product, display_properties)
        _display_product('Least expensive product', least_expensive_product, display_properties)
        _display_product('Most common product', most_common_product, display_properties)
        _display_product('Least common product', least_common_product, display_properties)
        print(f'Average Product Price: ${average_product_price / 100: 0.2f}')
        Menu.pause_console()


class BackupDatabase(MenuItem):
    """
    Functor for Backing up the database.
    """

    def execute(self) -> None:
        pass


def _determine_digit_length() -> int:
    digits = session.query(Product).count()
    digit_length = 0

    while digits > 0:
        digit_length += 1
        digits //= 10
    return digit_length


def _get_longest_product_name_length() -> int:
    longest_length = 0

    products = session.query(Product)
    for product in products:
        product_name_length = len(product.product_name.split(' - ')[0])

        if product_name_length > longest_length:
            longest_length = product_name_length

    return longest_length


def _get_longest_description_length() -> int:
    longest_length = 0

    products = session.query(Product)
    for product in products:
        product_description_length = 0
        if len(product.product_name.split(' - ')) > 1:
            product_description_length = len(product.product_name.split(' - ')[1])

        if product_description_length > longest_length:
            longest_length = product_description_length

    return longest_length


def _calculate_border_length() -> int:
    digit_length = _determine_digit_length() + 2
    gap_length = AppSetting.GAP_LENGTH.value
    name_length = _get_longest_product_name_length()
    description_length = _get_longest_description_length()
    return digit_length + gap_length + name_length + description_length


def _get_average_product_price():
    products = session.query(Product)
    total_number_of_products = session.query(Product).count()
    sum_of_product_prices = 0

    for product in products:
        sum_of_product_prices += product.product_price
    return sum_of_product_prices // total_number_of_products


def _display_product(characteristic: str, product, properties: list) -> None:
    border = ProductDisplay.BORDER_SYMBOL.value * _calculate_border_length()

    print(f'{border}')
    print(characteristic)
    print(border)
    for property in properties:
        if property == ProductDisplay.ID:
            print(f'ID      : {product.product_id}')
        if property == ProductDisplay.NAME:
            print(f'Name    : {product.product_name}')
        if property == ProductDisplay.PRICE:
            print(f'Price   : ${product.product_price / 100: 0.2f}')
        if property == ProductDisplay.QUANTITY:
            print(f'Quantity: {product.product_quantity}')
        if property == ProductDisplay.DATE:
            print(f'Updated : {product.date_updated.strftime("%m/%d/%Y")}')
    print(f'{border}\n')


def _get_valid_id() -> int:
    valid_inputs = [product.product_id for product in session.query(Product)]
    while True:
        try:
            user_input = int(input('Enter a product ID from the Inventory list: '))

            if user_input not in valid_inputs:
                raise ValueError
        except ValueError:
            print('Please enter a valid product ID from the list above.')
        else:
            return user_input


def _get_valid_price() -> int:
    price_error_exists = True
    price = None

    while price_error_exists:
        price = input('Enter the product price (ex. 9.75): ')
        price = clean.clean_price(price)
        if type(price) == int:
            price_error_exists = False
    return price


def _get_valid_quantity() -> int:
    quantity_error_exists = True
    quantity = None

    while quantity_error_exists:
        quantity = input('Enter quantity of product: ')
        quantity = clean.clean_quantity(quantity)
        if type(quantity) == int:
            quantity_error_exists = False
    return quantity


def _get_valid_date() -> datetime.date:
    date_error_exists = True
    date = None

    while date_error_exists:
        date = input('Enter the update date (02/21/1986): ')
        date = clean.clean_date(date)
        if type(date) == datetime.date:
            date_error_exists = False
    return date


if __name__ == '__main__':
    pass
