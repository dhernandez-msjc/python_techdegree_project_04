from models.menu import MenuItem
from models.model import (session, Product)

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
        products = session.query(Product)

        for product in products:
            print(product)


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
