from enum import Enum
from models.menu import (MenuItem, Menu)
from models.model import (session, Product)


class AppSetting(Enum):
    GAP_LENGTH = 7
    BORDER_SYMBOL = '>'


class NewProduct(MenuItem):
    """
    Functor for adding a new product to the database.
    """

    def execute(self) -> None:
        pass


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
        Menu.pause_console()


class ProductAnalysis(MenuItem):
    """
    Functor for displaying product analysis.
    """

    def execute(self) -> None:
        pass


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


if __name__ == '__main__':
    pass
