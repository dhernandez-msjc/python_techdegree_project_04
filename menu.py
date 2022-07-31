from string import ascii_letters
import os


class MenuItem:
    """
    Base class which stores a menu items description and has an
    overridable execute function to execute the action of the item.
    """

    def __init__(self, option_key: str, description: str) -> None:
        self.option_key = option_key
        self.description = description

    def execute(self) -> None:
        """
        Abstract method to execute the items actions.
        :return: None
        """
        pass


class Menu:
    """
    Menu class runs a given menu.
    """

    def __init__(self, title='Main Menu', border_symbol='~') -> None:
        self.menu_items = {}
        self.menu_item_keys = []
        self.menu_title = title
        self.border_symbol = border_symbol

    def add_menu_item(self, menu_item: MenuItem) -> None:
        self.menu_item_keys.append(menu_item.option_key)
        self.menu_items[menu_item.option_key] = menu_item

    def display_menu(self) -> None:
        EXTRA_GAP = 7
        border_length = self._determine_longest_line_length() + EXTRA_GAP
        border = border_length * self.border_symbol

        print('\n' + border)
        print(f'{self.menu_title: ^{border_length}}')
        print(border)
        for key in self.menu_item_keys:
            print(f'{key}) {self.menu_items[key].description}')
        print(border)

    def run_menu_selection(self, menu_choice: str) -> bool:
        if menu_choice in self.menu_item_keys:
            self.menu_items[menu_choice.upper()].execute()
            return True
        return False

    def start_menu(self) -> None:
        menu_is_running = True

        while menu_is_running:
            # self.clear_console()
            self.display_menu()

            user_selection = input('Enter a menu selection: ')
            menu_is_running = self.run_menu_selection(user_selection)

    @staticmethod
    def clear_console() -> None:
        command = 'cls' if os.name in ('nt', 'dos') else 'clear'
        os.system(command)

    @staticmethod
    def pause_console() -> None:
        input('\nPress enter to continue ...\n')

    def _determine_longest_line_length(self) -> int:
        longest_line_length = len(self.menu_title)

        for key, menu_item in self.menu_items.items():
            line_length = len(menu_item.description)
            if line_length > longest_line_length:
                longest_line_length = line_length
        return longest_line_length


class Testing(MenuItem):

    def execute(self) -> None:
        print("testing")


class QuitMenu(MenuItem):

    def execute(self, message='Closing the Application.') -> None:
        print(f'{message}')


if __name__ == '__main__':
    main_menu = Menu()
    main_menu.add_menu_item(Testing(option_key='A', description='Addition'))
    main_menu.add_menu_item(Testing(option_key='V', description='Another Addition'))
    main_menu.add_menu_item(QuitMenu(option_key='Q', description='Another Another Addition'))
    main_menu.start_menu()
