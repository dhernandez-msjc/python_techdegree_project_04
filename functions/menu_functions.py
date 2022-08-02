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


if __name__ == '__main__':
    build_main_menu()
