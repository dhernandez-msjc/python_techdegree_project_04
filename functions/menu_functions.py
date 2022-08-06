from models.menu import (MenuItem, Menu)
from functions.product_functions import (NewProduct, ViewProductById, ProductAnalysis,
                                         EditProduct, DeleteProduct, BackupDatabase)


def build_main_menu() -> None:
    main_menu = Menu()
    main_menu.add_menu_item(NewProduct('N', 'New Product'))
    main_menu.add_menu_item(ViewProductById('V', 'View Product by ID'))
    main_menu.add_menu_item(ProductAnalysis('A', 'Product Analysis'))
    main_menu.add_menu_item(BackupDatabase('B', 'Backup Database'))
    main_menu.add_exit_function(exit_message='''
    \rThank you for shopping with us!
    \rClosing the application.
    ''')
    main_menu.start_menu()


def build_edit_menu() -> None:
    product_edit_menu = Menu(title='Product Edit Meu', border_symbol='=')
    product_edit_menu.add_menu_item(EditProduct('E', 'Edit Current Product'))
    product_edit_menu.add_menu_item(DeleteProduct('D', DeleteProduct))
    product_edit_menu.add_exit_function(exit_name='Return to main menu')


if __name__ == '__main__':
    build_main_menu()
