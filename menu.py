import os


class MenuItem:
    """
    Base class which stores a menu items description and has an
    overridable execute function to execute the action of the item.
    """

    def __init__(self, description: str) -> None:
        self.description = description

    def execute(self) -> None:
        """
        Abstract method to execute the items actions.
        :return: None
        """
        pass


class QuitApplication(MenuItem):
    """
    Functor which provides an exit message when quitting application.
    """

    def execute(self):
        print('Thank you for shopping with us!')
        print('Closing the application.')


class Menu:
    """
    Menu class runs a given menu.
    """

    def __init__(self) -> None:
        self.menu_items = []

    def add_menu_item(self) -> None:
        pass

    def display_menu(self) -> None:
        pass

    def run_selection(self) -> None:
        pass

    def run_menu(self) -> None:
        pass


if __name__ == '__main__':
    menu_item = QuitApplication('Exit Menu')
    menu_item.execute()
