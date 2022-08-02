from menu_functions import (build_main_menu)
from cleaning_functions import add_csv_data
from model import (Base, engine)


def run_application() -> None:
    build_main_menu()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv_data('inventory.csv')
    run_application()
