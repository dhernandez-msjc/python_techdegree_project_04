import os

EXIT_KEY = 'Q'


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
        self.menu_items[menu_choice].execute()
        return menu_choice in self.menu_item_keys and menu_choice != EXIT_KEY

    def add_exit_function(self, exit_name='Exit', exit_message='Closing the Application.') -> None:
        if EXIT_KEY not in self.menu_item_keys:
            self.add_menu_item(QuitMenu(option_key=EXIT_KEY, description=exit_name, exit_message=exit_message))

    def start_menu(self) -> None:
        menu_is_running = True

        while menu_is_running:
            # self.clear_console()
            self.display_menu()
            user_selection = self._get_valid_user_entry()
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

    def _get_valid_user_entry(self) -> str:
        user_input = input('Enter a menu selection: ').upper()
        is_valid_input = user_input in self.menu_item_keys and len(user_input) == 1

        while not is_valid_input:
            print(f'''
            \rInvalid Menu Selection.
            \rPlease type in a valid entry: {self.menu_item_keys}
            ''')
            user_input = input('Enter a menu selection: ').upper()
            is_valid_input = user_input in self.menu_item_keys and len(user_input) == 1
        return user_input


class QuitMenu(MenuItem):

    def __init__(self, option_key: str, description: str, exit_message='Closing the Application') -> None:
        super().__init__(option_key, description)
        self.exit_message = exit_message

    def execute(self) -> None:
        print(f'{self.exit_message}')


if __name__ == '__main__':
    main_menu = Menu()
    main_menu.add_menu_item(QuitMenu(option_key='A', description='Addition', exit_message='Conquering world now.'))
    main_menu.add_exit_function()
    main_menu.start_menu()
