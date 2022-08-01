from menu import MenuItem


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
        pass


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


class QuitApplication(MenuItem):
    """
    Functor which provides an exit message when quitting application.
    """

    def execute(self):
        print('Thank you for shopping with us!')
        print('Closing the application.')


if __name__ == '__main__':
    menu_item = QuitApplication('Q', 'Quit Application')
    print(menu_item.option_key)
    menu_item.execute()
