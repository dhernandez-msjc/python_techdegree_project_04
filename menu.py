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
        self.menu_items = []
        self.menu_title = title
        self.border_symbol = border_symbol

    def add_menu_item(self, menu_item: MenuItem) -> None:
        self.menu_items.append(menu_item)

    def display_menu(self) -> None:
        border_length = self._determine_longest_line_length() + 7
        border = border_length * self.border_symbol

        print('\n' + border)
        print(f'{self.menu_title: ^{border_length}}')
        print(border)
        for menu_item in self.menu_items:
            print(f'{menu_item.option_key}) {menu_item.description}')
        print(border)

    def run_menu_selection(self) -> None:
        pass

    def start_menu(self) -> None:
        pass

    @staticmethod
    def clear_console() -> None:
        command = 'cls' if os.name in ('nt', 'dos') else 'clear'
        os.system(command)

    @staticmethod
    def pause_console() -> None:
        input('\nPress enter to continue ...\n')

    def _determine_longest_line_length(self) -> int:
        longest_line_length = 0

        for menu_item in self.menu_items:
            line_length = len(menu_item.description)
            if line_length > longest_line_length:
                longest_line_length = line_length
        return longest_line_length


if __name__ == '__main__':
    pass
