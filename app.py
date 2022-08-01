from functions.menu_functions import (build_main_menu)
from models.model import (Base, engine)


def run_application() -> None:
    build_main_menu()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    run_application()
