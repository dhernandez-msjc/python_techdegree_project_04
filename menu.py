import os


class MenuItem:

    def __init__(self, description: str) -> None:
        self.description = description

    def execute(self):
        pass


class ExitMenu(MenuItem):

    def execute(self):
        print('Thank you for shopping with us!')
        print('Closing the application.')


class Menu:

    def __init__(self) -> None:
        self.menu_items = []


if __name__ == '__main__':
    menu_item = ExitMenu('Exit Menu')
    menu_item.execute()
