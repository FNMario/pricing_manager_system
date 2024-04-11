import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import logging

logging.basicConfig(
    format=u'%(asctime)s %(levelname)-8s: %(message)s')


class DatabaseManager:

    def __init__(self):
        self.connection = None

    # Connection

    def login(self, username: str, password: str) -> dict[str, bool]:
        """
        Create a connection to the PostgreSQL database.

        Args:
            - username (str): A valid username.
            - password (str): Password for username.

        Returns:
            - permissions (dict[str,bool]): Pages the user has access to.
        """
        logging.info("Connecting to database.")
        host = os.getenv('PRICING_MANAGER_DB_SERVER', 'localhost')
        port = os.getenv('PRICING_MANAGER_DB_PORT', 5432)
        dbname = os.getenv('PRICING_MANAGER_DB_DATABASE', 'pricing_manager')
        try:
            self.connection = psycopg2.connect(
                host=host,
                port=port,
                dbname=dbname,
                user=username,
                password=password
            )
            logging.info(f"Successful connection as {username}.")
        except psycopg2.OperationalError as e:
            raise ConnectionError("Database Error - Login")

        cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        query = "SELECT * FROM user_permissions WHERE username = %s;"
        cursor.execute(query, (username,))
        logging.debug(cursor.query)
        data = cursor.fetchone()
        cursor.close()
        if data is None:
            return
        return dict(data)

    def logout(self) -> None:
        "Close connection if exist."
        if not self.connection:
            logging.warning("No active connection")
            return
        if not self.connection.closed:
            self.connection.close()
            logging.info("Database connection closed.")
        else:
            logging.info("Database connection already closed.")
        return

    # Products and costs

    def get_products_with_cost(self, product: str = None, local_code: str = None, supplier: str = None, supplier_code: str = None, section: str = None, from_date: str = None, to_date: str = None):
        """
        Return a list of products with costs. The list can be filtered with args.

        Args:
            - product (str): keywords to find in product name.
            - local_code (str): string of characters to search among local codes.
            - supplier (str): a supplier name.
            - supplier_code (str): string of characters to search among supplier codes.
            - section (str): a section name.
            - from_date (str), to_date (str): dates to search between them. Use format: 'yyyy-mm-dd'.

        Returns:
            list[tuple[str, str, str, str, float, str, float, float, str, datetime.date, float, str]]: list of products with the following data:
            - product: (str) product name.
            - local_code: (str) local product code.
            - supplier: (str) supplier name.
            - supplier_code: (str) supplier product code.
            - quantity: (float) quantity.
            - unit: (str) unit code name.
            - cost: (float) cost in pesos.
            - surcharge: (float) surcharge in decimal format. 1 = 100% = No surcharge, >1 = surcharge, <1 discount.
            - section: (str) section name.
            - date: (datetime.date) date when the record was inserted or modified.
            - dollar: (float) dollar price in pesos at the time of last price modification.
            - image_name: (str) name of image.
        """
        cursor = self.connection.cursor()
        filters = list()
        arguments = list()
        if product is not None:
            filters.append(
                "to_tsvector('simple', product) @@ to_tsquery('simple', %s)")
            words = [w for w in product.split(" ") if w != '']
            arguments.append(" & ".join(words))
        if local_code is not None:
            filters.append("local_code LIKE %s")
            arguments.append(local_code + "%")
        if supplier is not None:
            filters.append("supplier = %s")
            arguments.append(supplier)
        if supplier_code is not None:
            filters.append("supplier_code LIKE %s")
            arguments.append("%" + supplier_code + "%")
        if section is not None:
            filters.append("section = %s")
            arguments.append(section)
        if from_date is not None:
            filters.append("date >= %s")
            arguments.append(from_date)
        if to_date is not None:
            filters.append("date <= %s")
            arguments.append(to_date)
        query = "SELECT product, local_code, supplier, supplier_code, quantity, \
            unit, cost, surcharge, section, date, dollar_price, image_name \
            FROM list_of_products_with_costs WHERE " + \
            " AND ".join(filters) + ";"
        cursor.execute(query, tuple(arguments))
        logging.debug(cursor.query)
        data = cursor.fetchall()
        cursor.close()
        return data

    def get_products_for_sale(self, product: str = None, local_code: str = None, supplier_code: str = None):
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
        cursor = self.connection.cursor()
        filters = list()
        arguments = list()
        if product is not None:
            filters.append(
                "to_tsvector('simple', description) @@ to_tsquery('simple', %s)")
            words = [w for w in product.split(" ") if w != '']
            arguments.append(" & ".join(words))
        if local_code is not None:
            filters.append("code LIKE %s")
            arguments.append(local_code + "%")
        if supplier_code is not None:
            filters.append("suppliers_codes LIKE %s")
            arguments.append("%" + supplier_code + "%")
        query = "SELECT code, description, quantity, section, image_name, \
            suppliers_codes FROM list_of_products WHERE " + \
            " AND ".join(filters) + ";"
        cursor.execute(query, tuple(arguments))
        logging.debug(cursor.query)
        data = cursor.fetchall()
        cursor.close()
        return data

    def get_new_code(self, base: str) -> str:
        """
        Get the last used code for a given base.

        Args:
            - base: (str) prefix of the code. As minimum 4 digits, e.g., "AAA0".

        Returns:
            - next_code: (str) next code for new product.
        """
        if len(base) != 4:
            raise ValueError("Base must be at least 4 characters long.")
        cursor = self.connection.cursor()
        query = """
        SELECT %s || LPAD((MAX(SUBSTRING(code_id, 5)::integer) + 1)::text, 3, '0') AS next_code
        FROM products
        WHERE code_id LIKE %s;
        """
        cursor.execute(query, (base, base+"%"))
        logging.debug(cursor.query)
        data = cursor.fetchone()
        cursor.close()
        if data[0] is None:
            return base + "001"
        return data[0]

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
        cursor = self.connection.cursor()
        query = "SELECT quantity, unit, price, discount_level, date from get_product_price(%s);"
        cursor.execute(query, (product_code,))
        logging.debug(cursor.query)
        data = cursor.fetchone()
        cursor.close()
        return data

    def get_product(self, code_id: str) -> dict:
        """
        Return the product with the given code id.

        Args:
            code_id (str): local product code.

        Returns:
            product: Product information as a dict whit following keys:
            - 'description': (str) product description/name.
            - 'code_id': (str) local product code.
            - 'quantity': (float) quantity.
            - 'fraction_id': (int) fraction id.
            - 'section_id': (int) section id.
            - 'image_name': (str) name of image.
        """
        cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        query = """
        SELECT
            description,
            code_id,
            quantity,
            fraction_id,
            section_id,
            image_name
        FROM products
        WHERE
            code_id = %s;
        """
        cursor.execute(query, (code_id,))
        logging.debug(cursor.query)
        data = cursor.fetchone()
        cursor.close()
        if data is None:
            return
        return dict(data)

    def add_product(self, description: str, code_id: str, quantity: str, fraction_id: str, section_id: str, image_name: str) -> int:
        """
        Add a product in table products.

        Args:
            - description (str): product description/name.
            - code_id (str): local product code.
            - quantity (float): quantity.
            - fraction_id (int): fraction id.
            - section_id (int): section id.
            - image_name (str): name of image.

        Returns:
            rowcount: (int) the number of rows affected.
        """
        cursor = self.connection.cursor()
        query = """
        INSERT INTO 
        products (
            code_id, 
            description, 
            quantity, 
            fraction_id, 
            section_id, 
            image_name
        )
        VALUES
        (%s, %s, %s, %s, %s, %s);
        """
        cursor.execute(query,
                       (code_id, description, quantity,
                        fraction_id, section_id, image_name)
                       )
        logging.debug(cursor.query)
        self.connection.commit()
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount

    def alter_product(self, description: str, code_id: str, quantity: str, fraction_id: str, section_id: str, image_name: str) -> int:
        """
        Alter the product with given code_id in table 'products'. If the product does not exist, create it.

        Args:
            - description (str): product description/name.
            - code_id (str): local product code.
            - quantity (float): quantity.
            - fraction_id (int): fraction id.
            - section_id (int): section id.
            - image_name (str): name of image.

        Returns:
            rowcount: (int) the number of rows affected.
        """
        cursor = self.connection.cursor()
        query = """
        UPDATE products 
        SET
            description = %s,
            quantity = %s,
            fraction_id = %s,
            section_id = %s,
            image_name = %s
        WHERE 
            code_id = %s;
        """
        cursor.execute(query,
                       (description, quantity, fraction_id,
                        section_id, image_name, code_id)
                       )
        logging.debug(cursor.query)
        self.connection.commit()
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount

    def delete_product(self, code_id: str) -> int:
        """
        Delete the product with the given code_id in table 'products', and all the corresponding costs in table 'costs'.

        Args:
            - code_id (str): local product code.

        Returns:
            rowcount (int) the number of rows affected.
        """
        cursor = self.connection.cursor()
        query = "DELETE FROM products WHERE code_id = %s"
        cursor.execute(query, (code_id,))
        logging.debug(cursor.query)
        self.connection.commit()
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount

    def get_costs(self, product_id: str) -> list[tuple]:
        """
        Return the cost of the product with the given code id.

        Args:
            - product_id (str): local product code.

        Returns:
            list[tuple[str, int, str, float, date, float, float]]: information about the cost of all suppliers with the following data:
            - 'product_id': (str) local product code.
            - 'supplier_id': (int) supplier id.
            - 'supplier_code': (str) supplier product code.
            - 'cost': (float) cost in pesos.
            - 'surcharge': (date) surcharge in decimal format. 1 = 100% = No surcharge, >1 = surcharge, <1 discount.
            - 'date': (float) date of last modification.
            - 'dollar_price': (float) dollar price in pesos at the time of last price modification.
        """
        cursor = self.connection.cursor()
        query = """
        SELECT
            product_id, supplier_id, supplier_code,
            cost, surcharge, date, dollar_price
        FROM costs
        WHERE
            product_id = %s;
        """
        cursor.execute(query, (product_id,))
        logging.debug(cursor.query)
        data = cursor.fetchall()
        cursor.close()
        return data

    def get_cost(self, product_id: str, supplier_id: int) -> dict:
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
        cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        query = """
        SELECT
            product_id, supplier_id, supplier_code,
            cost, surcharge, date, dollar_price
        FROM costs
        WHERE
            product_id = %s
            AND supplier_id = %s;
        """
        cursor.execute(query, (product_id, supplier_id))
        logging.debug(cursor.query)
        data = cursor.fetchone()
        cursor.close()
        if data is None:
            return
        return dict(data)

    def add_cost(self, product_id: str, supplier_id: int, supplier_code: str, cost: float, surcharge: float, date: datetime.date, dollar_price: float) -> int:
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

        Returns:
            rowcount: (int) the number of rows affected.
        """
        cursor = self.connection.cursor()
        query = """
        INSERT INTO 
        costs (
            product_id, supplier_id, supplier_code,
            cost, surcharge, date, dollar_price
        )
        VALUES
        (%s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(query,
                       (product_id, supplier_id, supplier_code,
                        cost, surcharge, date, dollar_price)
                       )
        logging.debug(cursor.query)
        self.connection.commit()
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount

    def alter_cost(self, product_id: str, supplier_id: int, supplier_code: str, cost: float, surcharge: float, date: datetime.date, dollar_price: float) -> int:
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

        Returns:
            rowcount: (int) the number of rows affected.
        """
        cursor = self.connection.cursor()
        query = """
        UPDATE costs 
        SET
            supplier_code= %s,
            cost= %s,
            surcharge= %s,
            date= %s,
            dollar_price= %s
        WHERE 
            product_id = %s
            AND supplier_id= %s;
        """
        cursor.execute(query,
                       (supplier_code, cost, surcharge, date,
                        dollar_price, product_id, supplier_id)
                       )
        logging.debug(cursor.query)
        self.connection.commit()
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount

    def delete_cost(self, product_id: str, supplier_id: int) -> int:
        """
        Delete the cost of the supplier with the given supplier_id for the product with the given product_id.

        Args:
            - product_id (str): local product code.
            - supplier_id (int): supplier id.

        Returns:
            rowcount (int) the number of rows affected.
        """
        cursor = self.connection.cursor()
        query = "DELETE FROM costs WHERE product_id = %s AND supplier_id = %s;"
        cursor.execute(query, (product_id, supplier_id))
        logging.debug(cursor.query)
        self.connection.commit()
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount

    # Configurations

    def get_table_taxes(self) -> list[tuple]:
        """
        Get all taxes from the database and returns it as a list of tuples.

        Returns:
            A list of tuple containing all taxes from the database.
            Each tuple contains one line of the table in this order:
            - tax_id (int)
            - tax_name (str)
            - tax_value (float)
        """
        cursor = self.connection.cursor()
        query = "SELECT id, name, percentage FROM taxes;"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data

    def save_in_table_taxes(self, tax_name: str, value: float, id: int = None) -> int:
        """
        Save tax information into the 'taxes' table. If an 'id' is provided, update the existing record; otherwise create a new one.

        Args:
            - tax_name (str): name of tax.
            - value (float): decimal value (>0, <1).
            - id (int) (optional): entry id.

        Returns:
            rowcount (int) the number of rows affected.
        """
        cursor = self.connection.cursor()
        arguments = [tax_name, value]
        query = "INSERT INTO taxes (name, percentage"
        if id is not None:
            query += ", id"
            arguments.append(id)
        query += ") VALUES (%s, %s"
        if id is not None:
            query += ", %s"
        query += ")"
        if id is not None:
            query += " ON CONFLICT (id) DO UPDATE SET \
                name=EXCLUDED.name,  percentage=EXCLUDED.percentage"
        query += ";"
        cursor.execute(query, arguments)
        logging.debug(cursor.query)
        self.connection.commit()
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount

    def get_table_suppliers(self) -> list[tuple]:
        """
        Get all suppliers from the database and returns it as a list of tuples.

        Returns:
            A list of tuple containing all suppliers from the database.
            Each tuple contains one line of the table in this order:
            - supplier_id (int)
            - name (str)
            - phone (str)
            - email (str)
            - address (str)
        """
        cursor = self.connection.cursor()
        query = "SELECT id, name, phone, email, address FROM suppliers;"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data

    def save_in_table_suppliers(self, name: str, phone: str, email: str, address: str, id: int = None) -> int:
        """
        Save supplier information into the 'suppliers' table. If an 'id' is provided, update the existing record; otherwise create a new one.

        Args:
            - name (str): supplier's company name.
            - phone (str).
            - email (str).
            - address (str).
            - id (int): (optional) entry id.

        Returns:
            rowcount (int) the number of rows affected.
        """
        cursor = self.connection.cursor()
        arguments = [name, phone, email, address]
        query = "INSERT INTO suppliers (name, phone, email, address"
        if id is not None:
            query += ", id"
            arguments.append(id)
        query += ") VALUES (%s, %s, %s, %s"
        if id is not None:
            query += ", %s"
        query += ")"
        if id is not None:
            query += " ON CONFLICT (id) DO UPDATE SET \
                name=EXCLUDED.name,  phone=EXCLUDED.phone, \
                email=EXCLUDED.email,  address=EXCLUDED.address"
        query += ";"
        cursor.execute(query, arguments)
        logging.debug(cursor.query)
        self.connection.commit()
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount

    def get_table_fractions(self) -> list[tuple]:
        """
        Get all fractions from the database and returns it as a list of tuples.

        Returns:
            A list of tuple containing all fractions from the database.
            Each tuple contains one line of the table in this order:
            - fraction_id (int)
            - name (str)
            - description (str)
            - unit (str)
            - fraction_1 (float)
            - fraction_2 (float)
            - fraction_3 (float)
        """
        cursor = self.connection.cursor()
        query = "SELECT id, name, description, unit, fraction_1, fraction_2, fraction_3 FROM fractions;"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data

    def save_in_table_fractions(self, name: str, description: str, unit: str, fraction_1: float, fraction_2: float, fraction_3: float, id: int = None) -> int:
        """
        Save fraction information into the 'fractions' table. If an 'id' is provided, update the existing record; otherwise create a new one.

        Args:
            - name (str): 3 digits identifier.
            - description (str): brief description.
            - unit (str): written unit, not the abbreviation.
            - fraction_1 (float) fraction_2 (float) fraction_3 (float): quantity of (units) into which the product is divided. `-1` represents the closed package.
            - id (int): (optional) entry id.

        Returns:
            rowcount (int) the number of rows affected.
        """
        cursor = self.connection.cursor()
        arguments = [name, description, unit,
                     fraction_1, fraction_2, fraction_3]
        query = "INSERT INTO fractions (name, description, unit, fraction_1, fraction_2, fraction_3"
        if id is not None:
            query += ", id"
            arguments.append(id)
        query += ") VALUES (%s, %s, %s, %s, %s, %s"
        if id is not None:
            query += ", %s"
        query += ")"
        if id is not None:
            query += " ON CONFLICT (id) DO UPDATE SET \
                name=EXCLUDED.name,  description=EXCLUDED.description, \
                unit=EXCLUDED.unit,  fraction_1=EXCLUDED.fraction_1, \
                fraction_2=EXCLUDED.fraction_2,  fraction_3=EXCLUDED.fraction_3"
        query += ";"
        cursor.execute(query, arguments)
        logging.debug(cursor.query)
        self.connection.commit()
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount

    def get_table_sections(self) -> list[tuple]:
        """
        Get all sections from the database and returns it as a list of tuples.

        Returns:
            A list of tuple containing all sections from the database.
            Each tuple contains one line of the table in this order:
            - section_id (int)
            - name (str)
        """
        cursor = self.connection.cursor()
        query = "SELECT id, name FROM sections;"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data

    def save_in_table_sections(self, name: str, id: int = None) -> int:
        """
        Save section information into the 'sections' table. If an 'id' is provided, update the existing record; otherwise create a new one.

        Args:
            - name (str): name of section.
            - id (int): (optional) entry id.

        Returns:
            rowcount (int) the number of rows affected.
        """
        cursor = self.connection.cursor()
        arguments = [name]
        query = "INSERT INTO sections (name"
        if id is not None:
            query += ", id"
            arguments.append(id)
        query += ") VALUES (%s"
        if id is not None:
            query += ", %s"
        query += ")"
        if id is not None:
            query += " ON CONFLICT (id) DO UPDATE SET \
                name=EXCLUDED.name"
        query += ";"
        cursor.execute(query, arguments)
        logging.debug(cursor.query)
        self.connection.commit()
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount

    # Clients and Budgets

    def get_table_clients(self) -> list[tuple]:
        """
        Get all clients from the database and returns it as a list of tuples.

        Returns:
            A list of tuple containing all clients from the database.
            Each tuple contains one line of the table in this order:
            - cuit_cuil (str)
            - name (str)
            - email (str)
            - phone (str)
            - zip_code (int)
            - city (str)
            - address (str)
        """
        cursor = self.connection.cursor()
        query = "SELECT cuit_cuil, name, email, phone, zip_code, city, address FROM clients;"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data

    def get_client(self, cuit_cuil: str) -> list[tuple]:
        """
        Get client information by CUIT/CUIL.

        Args:
            - cuit_cuil (str): CUIT/CUIL without '-' nor ' ' (11 digits long).

        Returns:
            A list of tuple containing all clients from the database.
            Each tuple contains one line of the table in this order:
            - cuit_cuil (str)
            - name (str)
            - email (str)
            - phone (str)
            - zip_code (int)
            - city (str)
            - address (str)
        """
        if len(cuit_cuil) != 11:
            raise ValueError("cuit_cuil must be 11 characters long.")
        cursor = self.connection.cursor()
        query = "SELECT cuit_cuil, name, email, phone, zip_code, city, address FROM clients WHERE cuit_cuil like %s;"
        cursor.execute(query, ("%"+cuit_cuil+"%",))
        data = cursor.fetchall()
        cursor.close()
        return data

    def save_client(self, cuit_cuil: str, name: str, email: str, phone: str, zip_code: int, city: str, address: str) -> int:
        """
        Save client information into the 'clients' table. If cuit_cuil already exist in database it will update all other fields.
        Args:
            - cuit_cuil (str)
            - name (str)
            - email (str)
            - phone (str)
            - zip_code (int)
            - city (str)
            - address (str)

        Returns:
            rowcount (int) the number of rows affected.
        """
        cursor = self.connection.cursor()
        query = """
        INSERT INTO clients 
        (cuit_cuil, name, email, phone, zip_code, city, address) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (cuit_cuil) DO UPDATE SET 
            name=EXCLUDED.name,
            email=EXCLUDED.email,
            phone=EXCLUDED.phone,
            zip_code=EXCLUDED.zip_code,
            city=EXCLUDED.city,
            address=EXCLUDED.address;
        """
        arguments = (cuit_cuil, name, email, phone, zip_code, city, address)
        cursor.execute(query, arguments)
        logging.debug(cursor.query)
        self.connection.commit()
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount

    def get_budgets(self, budget_number: int = None, name: str = None, from_date=None, to_date=None) -> list[tuple]:
        """
        Retrieve budgets filtered by budget number, name and date range.

        Args:
            - budget_number (int): budget number.
            - name (str): Name of the client.
            - from_date (str), to_date (str): dates to search between them. Use format: 'yyyy-mm-dd'.


        Returns:
            A list of tuples representing each found budget with following format:
            - budget_number (int)
            - name (str)
            - date (str)
            - phone (str)
            - email (str)
            - address (str)
            - additional_discount (float)
            - client_cuit-cuil (str)
        """
        cursor = self.connection.cursor()
        filters = list()
        arguments = list()
        if name is not None:
            filters.append(
                "to_tsvector('simple', name) @@ to_tsquery('simple', %s)")
            words = [w for w in name.split(" ") if w != '']
            arguments.append(" & ".join(words))
        if budget_number is not None:
            filters.append("id::text LIKE %s")
            arguments.append("%" + budget_number + "%")
        if from_date is not None:
            filters.append("date >= %s")
            arguments.append(from_date)
        if to_date is not None:
            filters.append("date <= %s")
            arguments.append(to_date)
        if len(filters) == 0:
            query = "SELECT b.id, COALESCE(b.name, cl.name), b.date, \
                b.phone, b.email, b.address, b.additional_discount, b.client_cuit_cuil \
                FROM budgets AS b \
                LEFT JOIN clients AS cl ON b.client_cuit_cuil = cl.cuit_cuil \
                ORDER BY date DESC;"
        else:
            query = "SELECT b.id, COALESCE(b.name, cl.name), b.date, \
                b.phone, b.email, b.address, b.additional_discount, b.client_cuit_cuil \
                FROM budgets as b \
                LEFT JOIN clients as cl ON b.client_cuit_cuil = cl.cuit_cuil \
                WHERE " + " AND ".join(filters) + " ORDER BY date DESC;"
        cursor.execute(query, tuple(arguments))
        logging.debug(cursor.query)
        data = cursor.fetchall()
        cursor.close()
        return data

    def save_budget(self, budget_number: int, name: str = None, phone: str = None, email: str = None, address: str = None, client_cuit_cuil: str = None, additional_discount: float = 0) -> int:
        """
        Updates the budget information with the given id, in the 'budgets' table.

        Args:
            - budget_number (int): The number of the budget.
            - name (str): customer/company name.
            - phone (str): customer/company phone.
            - email (str): customer/company email.
            - address (str): customer/company address.
            - client_cuit_cuil (str): customer/company cuit or cuil.
            - additional_discount (float): (optional) additional discount if any.

        Returns:
            rowcount (int) the number of rows affected.
        """
        cursor = self.connection.cursor()
        query = """
        INSERT INTO budgets (
            id, name, phone, email, address,
            additional_discount, client_cuit_cuil
            ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET 
            name=EXCLUDED.name,
            phone=EXCLUDED.phone,
            email=EXCLUDED.email,
            address=EXCLUDED.address,
            additional_discount=EXCLUDED.additional_discount,
            client_cuit_cuil=EXCLUDED.client_cuit_cuil;
        """
        arguments = (
            budget_number, name, phone, email, address,
            additional_discount, client_cuit_cuil
        )
        cursor.execute(query, arguments)
        logging.debug(cursor.query)
        self.connection.commit()
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount

    def add_budget(self, name: str = None, phone: str = None, email: str = None, address: str = None, client_cuit_cuil: str = None, additional_discount: float = 0) -> int:
        """
        Adds a new budget into the database.

        Args:
            - name (str): customer/company name.
            - phone (str): customer/company phone.
            - email (str): customer/company email.
            - address (str): customer/company address.
            - client_cuit_cuil (str): customer/company cuit or cuil.
            - additional_discount (float): (optional) additional discount if any.

        Returns:
            budget_number (int): The number id  of the created budget.
        """
        cursor = self.connection.cursor()
        query = """
        INSERT INTO budgets (
            name, phone, email, address,
            additional_discount, client_cuit_cuil
            ) 
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
        """
        arguments = (
            name, phone, email, address,
            additional_discount, client_cuit_cuil
        )
        cursor.execute(query, arguments)
        logging.debug(cursor.query)
        self.connection.commit()
        budget_number = cursor.fetchone()[0]
        cursor.close()
        return budget_number

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
        cursor = self.connection.cursor()
        query = """
        SELECT 
            product_id, quantity, unit_price,
            sales_category_id, description, fraction_level
        FROM budget_items
        WHERE budget_id = %s;
        """
        cursor.execute(query, (budget_number,))
        data = cursor.fetchall()
        cursor.close()
        return data

    def save_budget_items(self, budget_number: int, items: list[tuple]) -> int:
        """
        Save a list of budget items into the database.

        Args:
            - budget_number (int): The unique identifier for a budget.
            - items (list[tuple]): List of products as tuples with following information:
                - local_code: (str) local product code.
                - quantity: (float) quantity.
                - unit_price: (float) price per unit in pesos.
                - sales_category_id: (int) [1, 2, 3] represent the category of client, used to calculate discount.
                - description: (str) description of the product.
                - fraction_level: (int) [0, 1, 2] level of fractions.

        Returns:
            rowcount (int) the number of rows affected.
        """
        cursor = self.connection.cursor()
        query = """
        INSERT INTO budget_items (
            product_id, budget_id, quantity, unit_price,
            sales_category_id, description, fraction_level
            ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        items = [(item[0], budget_number, *item[1:]) for item in items]
        cursor.executemany(query, items)
        logging.debug(cursor.query)
        if cursor.rowcount == len(items):
            self.connection.commit()
            rowcount = cursor.rowcount
        else:
            self.connection.cancel()
            rowcount = 0
        cursor.close()
        return rowcount

    def drop_budget_items(self, budget_number: int, items_codes: list[str]) -> None:
        """
        Remove from a budget some items identified by their codes.

        Args:
            - budget_number (int): The unique identifier for a budget.
            - items_codes (list[str]): list of codes of products to delete.
        """
        cursor = self.connection.cursor()

        query = "DELETE FROM budget_items WHERE budget_id = %s AND product_id = %s;"
        codes_list = [(budget_number, code) for code in items_codes]
        cursor.executemany(query, codes_list)
        if cursor.rowcount == len(items_codes):
            self.connection.commit()
            rowcount = cursor.rowcount
        else:
            self.connection.cancel()
            rowcount = 0
        cursor.close()
        return rowcount

    # Tables to print

    def get_tables_to_print_names(self, section_id: int, name: str = None) -> list[str]:
        """
            Get all tables names that match section and name.
        Args:
            - section_id (int): section id.
            - name (str): table name.

        Return:
            - table_names: list of strings/tuples with table names
        """
        cursor = self.connection.cursor()
        arguments = [section_id]
        query = """
        SELECT id, name
        FROM tables_to_print_names
        WHERE section_id = %s
        """
        if name:
            query += " AND UPPER(name) LIKE UPPER(%s)"
            arguments.append("%"+name+"%")
        query += ";"
        cursor.execute(query, arguments)
        data = cursor.fetchall()
        cursor.close()
        return data

    def get_tables_to_print_columns(self, table_id: int):
        """
        Return columns related to a specific table id.

        Args:
            - table_id (int): Table's unique identifier.

        Returns:
            - headers_checked: (list[str]) list of headers checked, ordered.
        """
        cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        query = """
        SELECT 
            venta_1, venta_2, venta_3,
            descuento_1, descuento_2, descuento_3,
            mayorista_1, mayorista_2, mayorista_3,
            fraccion_1, fraccion_2, fraccion_3, fecha
        FROM tables_to_print_names
        WHERE id = %s;
        """
        cursor.execute(query, (table_id,))
        data = cursor.fetchone()
        my_dict = dict(data)
        valid_keys = [key for key, value in my_dict.items()
                      if value is not None]
        sorted_keys = sorted(valid_keys, key=lambda key: my_dict[key])
        cursor.close()
        return sorted_keys

    def get_tables_to_print_items(self, table_id: int):
        """
        Return items related to a specific table id.

        Args:
            - table_id (int): Table's unique identifier.

        Returns:
            - products: (list[str])
        """
        cursor = self.connection.cursor()
        query = """
        SELECT 
            product_id, description
        FROM tables_to_print_items
        WHERE table_id = %s;
        """
        cursor.execute(query, (table_id,))
        data = cursor.fetchall()
        cursor.close()
        return data

    def add_tables_to_print_name(self, section_id: int, name: str) -> int:
        """
        Add new table in the specified section. If this table name already exists in that section, nothing happens.

        Args:
            - section_id (int): Section id where you want to put your table.
            - name (str): Name of the table.

        Returns:
            table_id (int): id of created table.
        """
        cursor = self.connection.cursor()
        query = """
        INSERT INTO tables_to_print_names (section_id, name) 
        VALUES (%s, %s)
        RETURNING id;
        """
        arguments = (section_id, name)
        cursor.execute(query, arguments)
        logging.debug(cursor.query)
        self.connection.commit()
        table_id = cursor.fetchone()[0]
        cursor.close()
        return table_id

    def save_tables_to_print_name(self, table_id: int, new_name: str):
        """
        Change table name in the given section.

        Args:
            - table_id (int): Section id where you want to put your table.
            - new_name (str): New name of the table.

        Returns:
            rowcount (int) the number of rows affected.
        """
        cursor = self.connection.cursor()
        query = """
        UPDATE tables_to_print_names 
        SET name = %s
        WHERE id = %s;
        """
        arguments = (new_name, table_id)
        cursor.execute(query, arguments)
        logging.debug(cursor.query)
        self.connection.commit()
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount

    def save_tables_to_print_columns(self, table_id: int, headers: list[str]) -> int:
        """
        Save new table data or update an existing one in the database.

        Args:
        - table_id (int): Identifier of the table.
        - headers (list[str]): List of string representing the header of each column in order. Accepted columns:
            - venta_1
            - venta_2
            - venta_3
            - descuento_1
            - descuento_2
            - descuento_3
            - mayorista_1
            - mayorista_2
            - mayorista_3
            - fraccion_1
            - fraccion_2
            - fraccion_3
            - fecha

        Returns:
            rowcount (int) the number of rows affected.
        """
        cursor = self.connection.cursor()
        query = """
        UPDATE tables_to_print_names
        SET
            venta_1 = %(venta_1)s,
            venta_2 = %(venta_2)s,
            venta_3 = %(venta_3)s,
            descuento_1 = %(descuento_1)s,
            descuento_2 = %(descuento_2)s,
            descuento_3 = %(descuento_3)s,
            mayorista_1 = %(mayorista_1)s,
            mayorista_2 = %(mayorista_2)s,
            mayorista_3 = %(mayorista_3)s,
            fraccion_1 = %(fraccion_1)s,
            fraccion_2 = %(fraccion_2)s,
            fraccion_3 = %(fraccion_3)s,
            fecha = %(fecha)s
        WHERE id = %(table_id)s;
        """
        arguments = {
            'venta_1': None,
            'venta_2': None,
            'venta_3': None,
            'descuento_1': None,
            'descuento_2': None,
            'descuento_3': None,
            'mayorista_1': None,
            'mayorista_2': None,
            'mayorista_3': None,
            'fraccion_1': None,
            'fraccion_2': None,
            'fraccion_3': None,
            'fecha': None,
            'table_id': table_id
        }
        for pos, column in enumerate(headers):
            arguments[column] = pos
        cursor.execute(query, arguments)
        self.connection.commit()
        logging.debug(cursor.query)
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount

    def save_tables_to_print_items(self, table_id: int, products: list[tuple]):
        """
        Save new table data or update an existing one in the database.

        Args:
        - table_id (int): Identifier of the table.
        - products (list[tuple[]): List of products as tuples with format (code, description).
        """
        cursor = self.connection.cursor()
        delete_query = "DELETE FROM tables_to_print_items WHERE table_id = %s;"
        cursor.execute(delete_query, (table_id,))
        add_query = """
        INSERT INTO tables_to_print_items (
            product_id, description, table_id
            ) 
        VALUES (%s, %s, %s);
        """
        items = [(*item, table_id) for item in products]
        cursor.executemany(add_query, items)
        logging.debug(cursor.query)
        if cursor.rowcount == len(items):
            self.connection.commit()
            rowcount = cursor.rowcount
        else:
            self.connection.cancel()
            rowcount = 0
        cursor.close()
        return rowcount
