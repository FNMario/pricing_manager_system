import datetime


class DatabaseManager:

    def __init__(self):
        self.connection = None

    # Users

    def login(self, username, password):
        """
        Create a connection to the PostgreSQL database.

        Args:
            - username (str): A valid username.
            - password (str): Password for username.

        Returns:
            - permissions (dict): Pages the user has access to.
        """
        pass

    # Products and costs

    def get_products_with_cost(self, **kwargs):
        """
        Return a list of products with costs. The list can be filtered with args.

        Args:
            - product (str): keywords to find in product name.
            - local_code (str): string of characters to search among local codes.
            - supplier_code (str): string of characters to search among supplier codes.
            - supplier (str): a supplier name.
            - section (str): a section name.
            - from_date (str), to_date (str): dates to search between them.

        Returns:
            list[tuple[str, str, str, str, float, str, float, float, str, datetime.date, float, str]]: list of products with the following data:
            - product: (str) product name.
            - local_code: (str) local product code.
            - supplier: (str) supplier name.
            - supplier_code: (str) supplier product code.
            - quantity: (float) quantity.
            - unit_name: (str) unit name.
            - price: (float) cost in pesos.
            - surcharge: (float) surcharge in decimal format. 1 = 100% = No surcharge, >1 = surcharge, <1 discount.
            - section: (str) section name.
            - date: (datetime.date) date when the record was inserted or modified.
            - dollar: (float) dollar price in pesos at the time of last price modification.
            - image_name: (str) name of image.
        """
        pass

    def get_products_for_sale(self, **kwargs):
        """
        Return a list of products. The list can be filtered with args.

        Args:
            - product (str): keywords to find in product name.
            - local_code (str): string of characters to search among local codes.
            - supplier_code (str): string of characters to search among supplier codes.

        Returns:
            list[tuple[str, str, str, str, float, str, float, float, str, datetime.date, float, str]]: list of products with the following data:
            - local_code: (str) local product code.
            - description: (str) product name.
            - quantity: (float) quantity with unit.
            - section: (str) section name.
            - image_name: (str) name of image.
            - suppliers_codes: (str) suppliers product codes.
        """
        pass

    def get_last_code(self, base: str) -> str:
        """
        Get the last used code for a given base.

        Args:
            - base: (str) prefix of the code.

        Returns:
            - next_code: (str) next code for new product.
        """
        pass

    def get_product_prices(self, product_code: str):
        """
        Return the sell prices for the  given product code.

        Args:
            - product_code (str): local product code.

        Returns:
            tuple[float, str, float, int, date]: Product information as a tuple whit following data:
            - quantity: (float) quantity.
            - unit: (str) 3 digit unit code.
            - price: (float) sell price in pesos.
            - discount_level: (int) level of discount applied (for wholesale sales).
            - date: (date) date of last change.
        """
        pass

    def get_product(self, code_id: str):
        """
        Return the product with the given code id.

        Args:
            code_id (str): local product code.

        Returns:
            tuple[str, str, float, int, int]: Product information as a tuple whit following data:
            - 'description': (str) product description/name.
            - 'code_id': (str) local product code.
            - 'quantity': (float) quantity.
            - 'fraction_id': (int) fraction id.
            - 'section_id': (int) section id.
            - image_name: (str) name of image.
        """
        pass

    def add_product(self, description: str, code_id: str, quantity: str, fraction_id: str, section_id: str):
        """
        Add a product in table products.

        Args:
            - description (str): product description/name.
            - code_id (str): local product code.
            - quantity (float): quantity.
            - fraction_id (int): fraction id.
            - section_id (int): section id.
            - image_name (str): name of image.
        """
        pass

    def alter_product(self, description: str, code_id: str, quantity: str, fraction_id: str, section_id: str):
        """
        Alter the product with given code_id in table 'products'. If the product does not exist, create it.

        Args:
            - description (str): product description/name.
            - code_id (str): local product code.
            - quantity (float): quantity.
            - fraction_id (int): fraction id.
            - section_id (int): section id.
            - image_name (str): name of image.
        """
        pass

    def delete_product(self, product_id: str):
        """
        Delete the product with the given product_id in table 'products', and all the corresponding costs in table 'costs'.

        Args:
            - product_id (str): local product code.
        """
        pass

    def get_cost(self, product_id, supplier_id):
        """
        Return the cost of the product with the given code id.

        Args:
            - product_id (str): local product code.
            - supplier_id (int): supplier id.

        Returns:
            tuple[str, int, str, float, date, float, float]: information about the cost as tuple with the following data:
            - 'product_id': (str) local product code.
            - 'supplier_id': (int) supplier id.
            - 'supplier_code': (str) supplier product code.
            - 'cost': (float) cost in pesos.
            - 'surcharge': (date) surcharge in decimal format. 1 = 100% = No surcharge, >1 = surcharge, <1 discount.
            - 'date': (float) date of last modification.
            - 'dollar_price': (float) dollar price in pesos at the time of last price modification.
        """
        pass

    def add_cost(self, product_id: str, supplier_id: int, supplier_code: str, cost: float, surcharge: float, date: datetime.date, dollar_price: float):
        """
        Add new values on costs table.

        Args:
            - product_id (str): local product code.
            - supplier_id (int): supplier id.
            - supplier_code (str): supplier product code.
            - cost (float): cost in pesos.
            - surcharge (float): surcharge in decimal format. 1 = 100% = No surcharge, >1 = surcharge, <1 discount.
            - date (date): date of creation.
            - dollar_price (float): dollar price in pesos at the time of creation.
        """
        pass

    def alter_cost(self, product_id: str, supplier_id: int, supplier_code: str, cost: float, surcharge: float, date: datetime.date, dollar_price: float):
        """
        Alter values on costs table.

        Args:
            - product_id (str): local product code.
            - supplier_id (int): supplier id.
            - supplier_code (str): supplier product code.
            - cost (float): cost in pesos.
            - surcharge (float): surcharge in decimal format. 1 = 100% = No surcharge, >1 = surcharge, <1 discount.
            - date (date): date of creation.
            - dollar_price (float): dollar price in pesos at the time of creation.
        """
        pass

    def delete_cost(self, product_id, supplier_id):
        """
        Delete the cost of the supplier with the given supplier_id for the product with the given product_id.

        Args:
            - product_id (str): local product code.
            - supplier_id (int): supplier id.
        """
        pass

    # Configurations

    def get_table(self, table_name: str) -> list[tuple]:
        """
        Get a specific table from database.

        Args:
        - table_name (str): name of the table to be returned.

        Returns:
            A table in format list[tuple]
        """
        pass

    def save_in_table(self, table_name: str, data: dict, id: int = None):
        """
        if 'id' is given, update an entry in table 'table' in columns given in 'data'. Else, new entry is created.

        Args:
            - table_name (str): name of table.
            - data (dict): dict with column names and respective data.
            - id (int): (optional) entry id.
        """
        pass

    # Clients and Budgets

    def get_client(self, id: int) -> list[tuple]:
        """
        Get client information by CUIT/CUIL.

        Args:
            - id (str): CUIT/CUIL without '-' nor ' '.

        Returns:
            Client information as tuple.
        """
        pass

    def save_client(self, data):
        """
        Save client information on clients table.

        Args:
            - data (dict): dictionary containing all necessary fields.
        """
        pass

    def get_budgets(self, budget_number: int = None, name: str = None, from_date=None, to_date=None) -> list[tuple]:
        """
        Retrieve budgets filtered by budget number, name and date range.

        Args:
            - budget_number (int): budget number.
            - name (str): Name of the client.
            - from_date (datetime): Initial date for filter.
            - to_date (datetime): Final date for filter.

        Returns:
            A list of tuples representing each found budget with following format:
            - budget_number (int)
            - name (str)
            - date (datetime.date)
            - phone (str)
            - email (str)
            - address (str)
            - additional_discount (float)
            - client_cuit-cuil (str)
        """
        pass

    def save_budget(self, budget_data: dict):
        """
        Saves an existing budget in database.

        Args:
            - budget_data (dict): a dictionary that contains all fields needed. 
        """
        pass

    def add_budget(self, budget_data: dict) -> int:
        """
        Adds a new budget into the database.

        Args:
            - budget_data (dict): a dictionary that contains all fields needed.

        Returns:
            The id number of the created budget.
        """
        pass

    def get_budget_items(self, budget_number: int) -> list[tuple]:
        """
        Get items related to a specific budget.

        Args:
            - budget_number (int): The unique identifier for a budget.

        Returns:
        A list with tuples, where each tuple represents one item on the budget. 
        Each tuple has the following structure:
            - local_code: (str) local product code.
            - quantity: (float) quantity.
            - unit_price: (float) price per unit in pesos.
            - sales_category_id: (int) [1, 2, 3] represent the category of client, used to calculate discount.
            - description: (str) description of the product.
            - fraction_level: (int) [0, 1, 2] level of fractions.
        """
        pass

    def save_budget_items(self, budget_number: int, items: list[tuple]):
        """
        Save a list of budget items into the database.

        Args:
            - budget_number (int): The unique identifier for a budget.
            - items (list[tuple]): List of tuples as described in `get_budget_items`.
        """
        pass

    def drop_budget_items(self, budget_number: int, items_codes: list[str]) -> None:
        """
        Remove from a budget some items identified by their codes.

        Args:
            - budget_number (int): The unique identifier for a budget.
            - items_codes (list[str]): list of codes of products to delete.
        """
        pass

    # Tables to print

    def get_tables_to_print_names(self, section: str, name: str = None) -> list[str]:
        """
            Get all tables names that match section and name.
        Args:
            - section (str): section name.
            - name (str): table name.

        Return:
            - table_names: list of strings with table names
        """
        pass

    def get_tables_to_print_data(self, table_id: int):
        """
        Return data related to a specific table id.

        Args:
            - table_id (int): Table's unique identifier.

        Returns:
            - headers_checked: (list[str])
            - products: (list[str])
        """
        pass

    def add_tables_to_print_name(self, section: str, name: str, id: int = None):
        """
        Add new table in the specified section. If this table name already exists in that section, it will replace it.

        Args:
            - section (str): Section where you want to put your table.
            - name (str): Name of the table.
        """
        # Return id?
        pass

    def save_table_to_print_data(self, table_id, headers, product_codes):
        """
            Save new table data or update an existing one in the database.

        Args:
        - table_id (int): Identifier of the table.
        - headers (list[str]): List of string representing the header of each column.
        - items_code (list[str]): List of product codes.
        """
        pass
