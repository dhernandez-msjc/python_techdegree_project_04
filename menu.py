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

    def execute(self):
        print('Thank you for shopping with us!')
        print('Closing the application.')


class Menu:
    """
    Menu class runs a given menu.
    """
    def __init__(self) -> None:
        self.menu_items = []


if __name__ == '__main__':
    menu_item = QuitApplication('Exit Menu')
    menu_item.execute()
