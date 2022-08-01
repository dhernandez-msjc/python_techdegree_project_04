import datetime
from models.menu import (MenuItem, Menu)


def build_main_menu() -> None:
    main_menu = Menu()
    main_menu.add_menu_item(MenuItem('N', 'New Product'))
    main_menu.add_menu_item(MenuItem('V', 'View All Products'))
    main_menu.add_menu_item(MenuItem('A', 'Product Analysis'))
    main_menu.add_menu_item(MenuItem('B', 'Backup Database'))
    main_menu.add_exit_function(exit_message='''
    \rThank you for shopping with us!
    \rClosing the application.
    ''')
    main_menu.start_menu()


def clean_product_id(product_id_string: str, available_options: list) -> int:
    pass


def clean_quantity(quantity_string: str) -> int:
    pass


def clean_price(price_string: str) -> int:
    pass


def clean_date(date_string: str) -> datetime.date:
    pass


def add_csv_data(csv_file_name: str) -> None:
    pass


if __name__ == '__main__':
    build_main_menu()
