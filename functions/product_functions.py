import datetime
import time
from enum import Enum
import functions.cleaning_functions as clean
from models.menu import (MenuItem, Menu)
from models.model import (session, Product)

# global variable to temporarily hold current product for editing
current_product = None


class AppSetting(Enum):
    """
    Enum for main application settings.
    """
    GAP_LENGTH = 7
    BORDER_SYMBOL = '>'


class ProductDisplay(Enum):
    """
    Enum for Product Display Settings
    """
    ID = Product.product_id
    NAME = Product.product_name
    PRICE = Product.product_price
    QUANTITY = Product.product_quantity
    DATE = Product.date_updated
    BORDER_SYMBOL = '~'


class ColumnName(Enum):
    """
    Enum for managing Columns
    """
    NAME = 'Name'
    PRICE = 'Price'
    QUANTITY = 'Quantity'
    DATE = 'Date'


def build_main_menu() -> None:
    """
    Function builds the main menu of the program.
    :return: None
    """
    main_menu = Menu()
    main_menu.add_menu_item(NewProduct('N', 'New Product'))
    main_menu.add_menu_item(ViewProductById('V', 'View Product by ID'))
    main_menu.add_menu_item(ViewProducts('P', 'View All Products'))
    main_menu.add_menu_item(ProductAnalysis('A', 'Product Analysis'))
    main_menu.add_menu_item(BackupDatabase('B', 'Backup Database'))
    main_menu.add_exit_function(exit_message='''
    \rThank you for shopping with us!
    \rClosing the application.
    ''')
    main_menu.start_menu()


def build_edit_menu() -> None:
    """
    Builds the edit menu allowing the user to rename the product, change the price,
    edit the quantity of product, the updated date, or delete the product.
    :return: None
    """
    product_edit_menu = Menu(title='Product Edit Meu', border_symbol='=')
    product_edit_menu.add_menu_item(DisplayProduct('V', 'View Product Details'))
    product_edit_menu.add_menu_item(EditProductName('N', 'Edit Product Name'))
    product_edit_menu.add_menu_item(EditProductPrice('P', 'Edit product price'))
    product_edit_menu.add_menu_item(EditProductQuantity('T', 'Edit product quantity'))
    product_edit_menu.add_menu_item(EditProductDate('U', 'Edit date updated'))
    product_edit_menu.add_menu_item(DeleteProduct('D', 'Delete Product'))
    product_edit_menu.add_exit_function(exit_name='Return to main menu', exit_message="Returning to main menu.")
    product_edit_menu.start_menu()


class NewProduct(MenuItem):
    """
    Functor for adding a new product to the database.
    """

    def execute(self) -> None:
        Menu.clear_console()
        product_name = input('Enter the product name: ')
        product_price = _get_valid_integer(prompt='Enter the product price (ex. 9.75): ',
                                           clean_function=clean.clean_price)
        product_quantity = _get_valid_integer(prompt='Enter quantity of product: ',
                                              clean_function=clean.clean_quantity)
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

        Menu.clear_console()
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
        Menu.pause_console()


class ViewProductById(MenuItem):
    """
    Allows selection of an individual product after view the product list.
    Temporarily stores selected product in global space, sets global variable
    to None upon returning to function close from edit_menu.
    """

    def execute(self) -> None:
        global current_product
        product_view = ViewProducts()
        product_view.execute()

        selected_product_id = _get_valid_id()
        current_product = session.query(Product).filter(Product.product_id == selected_product_id).first()
        displays = [ProductDisplay.NAME, ProductDisplay.PRICE, ProductDisplay.QUANTITY, ProductDisplay.DATE]
        Menu.clear_console()
        _display_product(f'Product ID: {current_product.product_id}', current_product, displays)
        build_edit_menu()
        current_product = None


class EditProductName(MenuItem):
    """
    Edits the product name in the database.
    """

    def execute(self) -> None:
        global current_product
        current_product.product_name = _edit_check(ColumnName.NAME, current_product.product_name)
        session.commit()


class EditProductPrice(MenuItem):
    """
    Edits the products price in the database.
    """

    def execute(self) -> None:
        global current_product
        current_product.product_price = _edit_check(ColumnName.PRICE, current_product.product_price)
        session.commit()


class EditProductQuantity(MenuItem):
    """
    Edits the product quantity in the database.
    """

    def execute(self) -> None:
        global current_product
        current_product.product_quantity = _edit_check(ColumnName.QUANTITY, current_product.product_quantity)
        session.commit()


class EditProductDate(MenuItem):
    """
    Edits the product update date.
    """

    def execute(self) -> None:
        global current_product
        current_product.product_date_updated = _edit_check(ColumnName.DATE, current_product.prodct_date_updated)
        session.commit()


class DeleteProduct(MenuItem):
    """
    Deletes current product from the database.
    """

    def execute(self) -> None:
        global current_product
        session.delete(current_product)
        session.commit()
        print('Product deleted')
        time.sleep(1.5)


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
        Menu.clear_console()
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
        db_backup_file_name = 'db_backup.csv'
        clean.write_csv(db_backup_file_name)
        print(f'Database has been successfully backed up to: {db_backup_file_name}')
        time.sleep(1.5)


class DisplayProduct(MenuItem):
    """
    Functor to display current product
    """

    def execute(self) -> None:
        global current_product
        displays = [ProductDisplay.NAME, ProductDisplay.PRICE, ProductDisplay.QUANTITY, ProductDisplay.DATE]

        if current_product is not None:
            _display_product(f'Product ID: {current_product.product_id}', current_product, displays)
        else:
            print('Product has been deleted.  Please select a new product.')

        Menu.pause_console()


def _edit_check(column_name: ColumnName, current_value):
    print(f'\n**** EDIT {column_name.value} ****')
    if column_name is column_name.PRICE:
        print(f'\rCurrent Value: {current_value / 100: 0.2f}')
    elif column_name is column_name.DATE:
        print(f'\rCurrent Value: {current_value.strftime("%m/%d/%Y")}')
    else:
        print(f'\rCurrent Value: {current_value}')

    if column_name is column_name.NAME:
        return input('What would you like to change the value to: ')
    else:
        changes = input('What would you like to change the value to: ')
        if column_name is column_name.PRICE:
            return clean.clean_price(changes)
        elif column_name is column_name.QUANTITY:
            return clean.clean_quantity(changes)
        else:
            return clean.clean_date(changes)


def _determine_digit_length() -> int:
    """
    Determines the number of digits in an integer.
    :return: integer representing the number of digits.
    """
    digits = session.query(Product).count()
    digit_length = 0

    while digits > 0:
        digit_length += 1
        digits //= 10
    return digit_length


def _get_longest_product_name_length() -> int:
    """
    Determines the length of the longest product name.
    :return: integer value representing the length.
    """
    longest_length = 0

    products = session.query(Product)
    for product in products:
        product_name_length = len(product.product_name.split(' - ')[0])

        if product_name_length > longest_length:
            longest_length = product_name_length

    return longest_length


def _get_longest_description_length() -> int:
    """
    Determines the longest description length of a product.
    :return: integer value representing the longest description length.
    """
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
    """
    Calculates the border length based on the total product name with clean
    spacing.  Also takes into account provided gap length and non-white spacing.
    :return:
    """
    digit_length = _determine_digit_length() + 2
    gap_length = AppSetting.GAP_LENGTH.value
    name_length = _get_longest_product_name_length()
    description_length = _get_longest_description_length()
    return digit_length + gap_length + name_length + description_length


def _get_average_product_price():
    """
    Determines the average product price.
    :return:
    """
    products = session.query(Product)
    total_number_of_products = session.query(Product).count()
    sum_of_product_prices = 0

    for product in products:
        sum_of_product_prices += product.product_price
    return sum_of_product_prices // total_number_of_products


def _display_product(characteristic: str, product, attributes: list) -> None:
    """
    Displays the individual product price in a nicely formatted manner.
    :param characteristic: The title of what is to be shown.
    :param product: The query result product to be shown.
    :param attributes: The desired attributes of the product to be displayed.
    :return: None
    """
    border = ProductDisplay.BORDER_SYMBOL.value * _calculate_border_length()

    print(f'\n{border}')
    print(characteristic)
    print(border)
    for attribute in attributes:
        if attribute == ProductDisplay.ID:
            print(f'ID      : {product.product_id}')
        if attribute == ProductDisplay.NAME:
            print(f'Name    : {product.product_name}')
        if attribute == ProductDisplay.PRICE:
            print(f'Price   : ${product.product_price / 100: 0.2f}')
        if attribute == ProductDisplay.QUANTITY:
            print(f'Quantity: {product.product_quantity}')
        if attribute == ProductDisplay.DATE:
            print(f'Updated : {product.date_updated.strftime("%m/%d/%Y")}')
    print(f'{border}')


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


def _get_valid_integer(prompt: str, clean_function):
    error_exists = True
    value = None

    while error_exists:
        value = input(prompt)
        value = clean_function(value)
        if type(value) is int:
            error_exists = False
    return value


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
