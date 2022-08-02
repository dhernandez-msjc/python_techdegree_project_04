from functions.menu_functions import (build_main_menu)
from functions.cleaning_functions import add_csv_data
from models.model import (Base, engine)


def run_application() -> None:
    build_main_menu()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv_data('models/data/inventory.csv')
    # run_application()
