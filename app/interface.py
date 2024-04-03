import datetime
from datetime import datetime as dt
from database import postgresql_scripts as sql
from screens.widgets.messagebox import MessageBox
import logging


db = sql.DatabaseManager()

# Users


def login(username, password):
    """
    Call the database function to fetch user data, create a connection and return user permissions.
    """
    permissions = db.login(username=username, password=password)
    return permissions


def create_new_user(username, password):
    """
    NOT IMPLEMENTED
    Call the database function to insert a new user
    """
    return (username, password)


def update_user_password(username, old_pass, new_pass):
    """
    NOT IMPLEMENTED
    Update user password
    """
    return (username, new_pass)


def logout():
    db.logout()


# Products


def get_products_for_sale(product: str = None, local_code: str = None, supplier_code: str = None) -> list[str]:
    products = db.get_products_for_sale(
        product=product, local_code=local_code, supplier_code=supplier_code)
    return products


def get_products(
    product: str = None,
    local_code: str = None,
    supplier_code: str = None,
    section: str = None,
    supplier: str = None,
    from_date: str = None,
    to_date: str = None
) -> list:
    search_fields = {
        'product': product,
        'local_code': local_code,
        'supplier_code': supplier_code,
        'supplier': supplier,
        'section': section,
        'from_date': dt.strptime(from_date, '%d/%m/%Y') if from_date else None,
        'to_date': dt.strptime(to_date, '%d/%m/%Y') if to_date else None
    }

    products = db.get_products_with_cost(**search_fields)
    products = [(*p[:9], p[9].strftime('%d/%m/%Y'), *p[10:]) for p in products]
    return products


def get_last_code(base: str) -> str:
    "Returns the next code in that base to create new product"
    return db.get_new_code(base)


def save_product(data: dict):
    units = {f[1]: f[0] for f in get_fractions()}
    sections = {key: value for value, key in get_sections()}
    suppliers = {_[1]: _[0] for _ in get_suppliers()}

    new_product = {
        'description': data['product'],
        'code_id': data['local_code'],
        'quantity': data['quantity'],
        'fraction_id': units[data['unit']],
        'section_id': sections[data['section']],
        'image_name': ''
    }

    new_cost = {
        'product_id': data['local_code'],
        'supplier_id': suppliers[data['supplier']],
        'supplier_code': data['supplier_code'],
        'cost': data['cost'],
        'surcharge': data['surcharge'],
        'date': dt.strptime(data['date'], '%d/%m/%Y') if data['date'] else dt.today(),
        'dollar_price': data['dollar']
    }

    old_product = db.get_product(code_id=new_product['code_id'])

    if not old_product:
        db.add_product(**new_product)
        db.add_cost(**new_cost)
        return

    if old_product['quantity'] != new_product['quantity'] or old_product['fraction_id'] != new_product['fraction_id']:
        raise ValueError(
            "quantity and/or fraction doesn't match with product code. Try new code or replace it")
    elif old_product != new_product:
        db.alter_product(**new_product)

    old_cost = db.get_cost(
        product_id=new_cost['product_id'], supplier_id=new_cost['supplier_id'])

    if not old_cost:
        db.add_cost(**new_cost)
    else:
        db.alter_cost(**new_cost)


def change_price(product_code: str, supplier: str, supplier_code: str, new_price: float, surcharge: float, date: str = None, dollar_price: float = None):
    suppliers = {_[1]: _[0] for _ in get_suppliers()}

    new_cost = {
        'product_id': product_code,
        'supplier_id': suppliers[supplier],
        'supplier_code': supplier_code,
        'cost': new_price,
        'surcharge': surcharge,
        'date':  dt.strptime(date, '%d/%m/%Y') if date else dt.today(),
        'dollar_price': dollar_price if dollar_price else get_dollar_price
    }

    db.alter_cost(**new_cost)


def delete_product(data: dict, all_costs: bool = False):
    # TODO: refactor function: manage messagebox in manage_prices.py
    def answer_clicked(answer):
        print(f'Perform action? {answer}')
        if answer == "Delete all" or answer == "Delete":
            try:
                for supplier_id in [cost[1] for cost in costs]:
                    db.delete_cost(
                        product_id=data['local_code'], supplier_id=supplier_id)
                db.delete_product(code_id=data['local_code'])
                pass
            except Exception as e:
                logging.error(e)
        elif answer == "Only this one":
            try:
                db.delete_cost(
                    product_id=data['local_code'], supplier_id=cost[1])
                pass
            except Exception as e:
                logging.error(e)
            pass
        else:
            logging.error("Canceled by the user")
    costs = db.get_costs(product_id=data['local_code'])
    if len(costs) > 1:
        message = f"There are {len(costs)} suppliers for this products:"
        suppliers = {_[0]: _[1] for _ in get_suppliers()}
        for cost in costs:
            message += f"\n- Supplier: {suppliers[cost[1]]:<15}, Cost: ${cost[3]:.2f} "
        buttons = ["Delete all", "Cancel"] if all_costs else [
            "Delete all", "Only this one", "Cancel"]
        msg = MessageBox(
            message=message,
            kind='question',
            buttons=buttons,
            on_close=answer_clicked
        )
    elif len(costs) == 1:
        msg = MessageBox(
            message=f"Are you sure you want to delete it?",
            kind='question',
            buttons=["Delete", "Cancel"],
            on_close=answer_clicked
        )
    else:
        answer_clicked("Delete all")


# Settings and tables


def get_ivas() -> list:
    return [tax[2] for tax in db.get_table_taxes()]


def save_ivas(iva: float, row: int = -1) -> bool:
    saved = 0
    added = 0
    if row > -1:
        saved = db.save_in_table_taxes(tax_name='', value=iva, id=row)
    else:
        added = db.save_in_table_taxes(tax_name='', value=iva)
    if saved:
        logging.info('Saved IVA')
    elif added:
        logging.info('Added new IVA')
    else:
        logging.error('Error while saving new IVA')
        return False
    return True


def get_dollars() -> list:
    global _dollars
    dollar_now = get_dollar_price()
    return [dollar_now] + _dollars


def save_dollars(dollar: float, row: int = -1) -> bool:
    global _dollars
    if 0 < row and row < len(_dollars):
        _dollars[row] = float(dollar)
        return True
    else:
        _dollars.append(dollar)
        return True
    return False


def get_suppliers() -> list[tuple]:
    suppliers = db.get_table_suppliers()
    for row, supplier in enumerate(suppliers):
        n_row = list()
        for col, value in enumerate(supplier):
            n_row.append(value if value is not None else '')
        suppliers[row] = tuple(n_row)
    return suppliers


def save_supplier(supplier: dict) -> bool:
    assert 'name' in supplier, "program_error."
    assert supplier['name'], "Name cannot be empty"
    assert 'phone' in supplier, "program_error."
    assert 'email' in supplier, "program_error."
    assert 'address' in supplier, "program_error."
    saved = 0
    added = 0
    if 'id' in supplier:
        assert supplier['id'], "id cannot be empty"
        id = int(supplier.pop('id'))
        saved = db.save_in_table_suppliers(id=id, **supplier)
    else:
        added = db.save_in_table_suppliers(**supplier)

    if saved:
        logging.info('Supplier %s has been successfully updated',
                     supplier['name'])
    elif added:
        logging.info('New supplier %s has been created', supplier['name'])
    else:
        logging.error('Error while updating/creating the supplier')
        return False
    return True


def get_fractions() -> list[tuple]:
    fractions = db.get_table_fractions()
    for row, fraction in enumerate(fractions):
        n_row = list()
        for col, value in enumerate(fraction):
            n_row.append(value if value is not None else '')
        fractions[row] = tuple(n_row)
    return fractions


def save_fraction(fraction: dict) -> bool:
    assert 'name' in fraction, "program_error."
    assert fraction['name'], "Name cannot be empty"
    assert 'description' in fraction, "program_error."
    assert 'unit' in fraction, "program_error."
    assert 'fraction_1' in fraction, "program_error."
    fraction['fraction_1'] = 0 if not fraction['fraction_1'] else float(
        fraction['fraction_1'])
    assert 'fraction_2' in fraction, "program_error."
    fraction['fraction_2'] = 0 if not fraction['fraction_2'] else float(
        fraction['fraction_2'])
    assert 'fraction_3' in fraction, "program_error."
    fraction['fraction_3'] = 0 if not fraction['fraction_3'] else float(
        fraction['fraction_3'])
    saved = 0
    added = 0
    if 'id' in fraction:
        assert fraction['id'], "id cannot be empty"
        id = int(fraction.pop('id'))
        saved = db.save_in_table_fractions(id=id, **fraction)
    else:
        added = db.save_in_table_fractions(**fraction)

    if saved:
        logging.info('Fraction %s has been successfully updated',
                     fraction['name'])
    elif added:
        logging.info('New fraction %s has been created', fraction['name'])
    else:
        logging.error('Error while updating/creating the fraction')
        return False
    return True


def get_sections() -> list[tuple]:
    sections = db.get_table_sections()
    for row, section in enumerate(sections):
        n_row = list()
        for col, value in enumerate(section):
            n_row.append(value if value is not None else '')
        sections[row] = tuple(n_row)
    return sections


def save_section(section: dict) -> bool:
    assert 'name' in section, "program_error."
    assert section['name'], "Name cannot be empty"
    saved = 0
    added = 0
    if 'id' in section:
        assert section['id'], "id cannot be empty"
        id = int(section.pop('id'))
        saved = db.save_in_table_sections(id=id, name=section['name'])
    else:
        added = db.save_in_table_sections(name=section['name'])

    if saved:
        logging.info('Section %s has been successfully updated',
                     section['name'])
    elif added:
        logging.info('New section %s has been created', section['name'])
    else:
        logging.error('Error while updating/creating the section')
        return False
    return True


def get_clients() -> list[tuple]:
    clients = db.get_table_clients()
    for row, client in enumerate(clients):
        n_row = list()
        for col, value in enumerate(client):
            n_row.append(value if value is not None else '')
        clients[row] = tuple(n_row)
    clients = [('-'.join([_[0][:2], _[0][2:10], _[0][10]]), *_[1:])
               for _ in clients]
    return clients


def get_client(cuit_cuil: str) -> list[tuple]:
    clients = db.get_client(cuit_cuil.replace('-', ''))
    clients = [('-'.join([_[0][:2], _[0][2:10], _[0][10]]), *_[1:])
               for _ in clients]
    return clients


def save_client(client: dict) -> bool:
    global _clients
    assert 'cuit_cuil' in client, "program_error"
    assert len(client['cuit_cuil'].replace('-', '')
               ) == 11, "cuit_cuil must be in format XX-XXXXXXXX-X"
    assert 'name' in client, "program_error."
    assert client['name'], "Name cannot be empty"
    assert 'phone' in client, "program_error."
    assert 'email' in client, "program_error."
    assert 'address' in client, "program_error."
    assert 'city' in client, "program_error."
    assert 'zip_code' in client, "program_error."
    client.update(
        {
            'cuit_cuil': client['cuit_cuil'].replace('-', ''),
            'zip_code': int(client['zip_code']) if client['zip_code'] else None,
            'name': client['name'].title()
        }
    )
    saved = db.save_client(**client)
    return bool(saved)


def get_budgets(budget_number: int, name: str, from_date: str, to_date: str) -> list[tuple]:
    budget_number = budget_number if budget_number else None
    name = name.strip().lower() if name else None
    from_date = datetime.strptime(from_date, '%d/%m/%Y') \
        if from_date else None
    to_date = datetime.strptime(to_date, '%d/%m/%Y') \
        if to_date else None
    budgets = db.get_budgets(budget_number, name, from_date, to_date)
    for row, budget in enumerate(budgets):
        new_row = [val if val else '' for val in budget]
        budgets[row] = tuple(new_row)
    return budgets


def get_budget_items(budget_number: int) -> list[tuple]:
    items = db.get_budget_items(budget_number)
    categories = {1: "V", 2: "D", 3: "M"}
    for row, item in enumerate(items):
        items[row] = (
            item[0],
            item[1],
            item[2],
            categories[item[3]],
            item[4],
            item[5],
        )
    return items


def save_budget(budget_data: dict, items: list) -> bool:
    has_cuit = budget_data['cuit_cuil'] != ""
    has_name = budget_data['name'] != ""
    has_budget_number = budget_data['budget_number'] > 0
    has_items = len(items) > 0
    assert has_cuit or has_name, "Budget must have a cuit and/or a name."
    assert has_items, "Budget must have at least one product."
    budget_data.update({
        'client_cuit_cuil': budget_data['cuit_cuil'] if budget_data['cuit_cuil'] else None
    })
    budget_data.pop('cuit_cuil', None)
    for key, val in budget_data.items():
        budget_data[key] = val if val else None
    if has_budget_number:
        db.save_budget(**budget_data)
        budget_number = budget_data['budget_number']
    else:
        budget_data.pop('budget_number', None)
        budget_number = db.add_budget(**budget_data)

    saved_items = db.get_budget_items(budget_number)
    items_to_drop = list()
    categories = {"V": 1, "D": 2, "M": 3}
    for row, item in enumerate(items):
        items[row] = (*item[:3], categories[item[3]], *item[4:])
    for item in saved_items:
        if item in items:
            items.remove(item)
        else:
            items_to_drop.append(item)

    if items_to_drop:
        items_codes = [item[0] for item in items_to_drop]
        db.drop_budget_items(budget_number, items_codes)
    if items:
        db.save_budget_items(budget_number, items)


def get_tables_to_print_names(section: str, name: str = None) -> list[str]:
    sections = get_sections()
    section_id = [id for id, _section in sections if _section == section][0]
    tables = db.get_tables_to_print_names(section_id, name)
    return tables


def get_table_to_print_data(table_id: int) -> tuple[list[str], list[str]]:
    columns_id = {
        "venta_1": "chk_client_1_fraction_1",
        "venta_2": "chk_client_1_fraction_2",
        "venta_3": "chk_client_1_fraction_3",
        "descuento_1": "chk_client_2_fraction_1",
        "descuento_2": "chk_client_2_fraction_2",
        "descuento_3": "chk_client_2_fraction_3",
        "mayorista_1": "chk_client_3_fraction_1",
        "mayorista_2": "chk_client_3_fraction_2",
        "mayorista_3": "chk_client_3_fraction_3",
        "fraccion_1": "chk_fraction_1",
        "fraccion_2": "chk_fraction_2",
        "fraccion_3": "chk_fraction_3",
        "fecha": "chk_date"
    }
    columns = db.get_tables_to_print_columns(table_id)
    columns = list(map(lambda _: columns_id[_], columns))
    rows = db.get_tables_to_print_items(table_id)
    return rows, columns


def add_tables_to_print_name(section: str, name: str):
    sections_id = {section: id for id, section in get_sections()}
    section_id = sections_id[section]
    try:
        table_id = db.add_tables_to_print_name(section_id, name)
        return table_id
    except:
        return False


def save_tables_to_print_name(table_id: int, new_name: str):
    saved = db.save_tables_to_print_name(table_id, new_name)
    return saved == 1


def save_table_to_print_data(table_id: int, items: list[tuple], headers: list[str]):
    # Save columns
    def header_formatting(string: str) -> str:
        replacements = {
            'á': 'a',
            'é': 'e',
            'í': 'i',
            'ó': 'o',
            'ú': 'u',
            ' ': '_'
        }
        for word, replacement in replacements.items():
            string = string.replace(word, replacement).lower()
        return string

    headers = list(map(header_formatting, headers))
    columns_saved = db.save_tables_to_print_columns(table_id, headers)

    # Save items
    items_saved = db.save_tables_to_print_items(table_id, items)

    return columns_saved, items_saved


def print_table(items, header):
    from tabulate import tabulate
    print(tabulate(items, headers=header, tablefmt="fancy_outline"))


# Prices

def _apply_discount(surcharge_level, fraction, category):
    discounts = [
        [
            [1, 0.97, 0.941],
            [1, 0.95, 0.9025],
            [1, 0.93, 0.8649],
            [1, 0.92, 0.8464],
            [1, 0.9, 0.81],
            [1, 0.7, 0.63],
            [1, 0.6, 0.54],
        ],
        [
            [0.955, 0.9268, 0.899],
            [0.926, 0.8799, 0.8345],
            [0.926, 0.8646, 0.8011],
            [0.9118, 0.8388, 0.7717],
            [0.9, 0.8077, 0.7269],
            [0.9, 0.63, 0.567],
            [0.9, 0.54, 0.486],
        ],
        [
            [0.9127, 0.8853, 0.8588],
            [0.8574, 0.8145, 0.7738],
            [0.8574, 0.7974, 0.7415],
            [0.8306, 0.7641, 0.703],
            [0.8044, 0.7239, 0.6515],
            [0.8044, 0.567, 0.5103],
            [0.8044, 0.486, 0.4374],
        ]
    ]

    if category < 3 and surcharge_level < 7 and fraction < 3:
        return discounts[category][surcharge_level][fraction]
    else:
        return None


def calculate_prices(quantity: float, unit: str, cost: float = None, price: float = None, surcharge: float = None, discount_level: int = None):
    "return de prices for different clients"

    prices = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]
    fractions = [0, 0, 0]
    str_unit = ''

    if (price and discount_level is not None) or (cost and surcharge):
        pass
    else:
        return prices, fractions, str_unit

    if surcharge is not None:
        if surcharge >= 0 and surcharge < 1.70:
            discount_level = 0
        elif surcharge < 2.00:
            discount_level = 1
        elif surcharge < 2.20:
            discount_level = 2
        elif surcharge < 2.50:
            discount_level = 3
        elif surcharge < 3.50:
            discount_level = 4
        elif surcharge < 4.50:
            discount_level = 5
        elif surcharge >= 4.50:
            discount_level = 6
        else:
            raise (ValueError("Surcharge must be bigger than 0"))
    elif discount_level is not None:
        if discount_level not in range(7):
            raise ValueError(
                "Invalid discount level. It must be between 0 and 6")
    else:
        raise (TypeError("You must provide surcharge or discount_level"))

    if price is None:
        price = cost * surcharge
    unit_price = price / quantity

    try:
        fractions_list = get_fractions()
        fraction_index = [_[1].strip()
                          for _ in fractions_list].index(unit.strip())
        fractions = list(map(float, fractions_list[fraction_index][4:7]))
        str_unit = fractions_list[fraction_index][3]
    except ValueError:
        fractions = [1, -1, 0]
        str_unit = unit

    for category in range(3):
        for fraction in range(3):
            if fractions[fraction] == -1:
                fractions[fraction] = quantity
            prices[fraction][category] = unit_price * fractions[fraction] * \
                _apply_discount(discount_level, fraction, category)

    return prices, fractions, str_unit


def round_prices(prices):
    return [[round(price_0), round(price_1), round(price_2)] for price_0, price_1, price_2 in prices]


def get_product_prices(product_code):

    try:
        quantity, unit, price, discount_level, date = db.get_product_prices(
            product_code)
    except:
        return [[0]*3]*3, ['-']*3, dt.strptime('01-01-1900', '%d-%m-%Y')

    prices, fractions, str_unit = calculate_prices(
        quantity=quantity, unit=unit, price=price, discount_level=discount_level)

    quantities = [f"{_} {str_unit}" for _ in fractions]

    return round_prices(prices), quantities, date


def format_numeric_economy(price: float, show_currency_symbol: bool = False, currency_symbol: str = "$") -> str:
    if not price:
        price = 0
    if show_currency_symbol:
        return f"{currency_symbol}{chr(0x2009)}{price:,.2f}".replace(",", chr(0x2009))
    else:
        return f"{price:,.2f}".replace(",", chr(0x2009))


# External

def get_date():
    return dt.strftime(dt.today(), '%d/%m/%Y')


def get_dollar_price():
    return 835  # TODO: scrape dolar price (done and staged)


# Listas temporales

_dollars = [800, 900]


_clients = [
    ('20231439389', 'Alejandro Mario', None, None, 3200, None, 'Italia 1576'),
    ('20480287631', 'Valentino Benicio Coronel', 'moralessantiago-benjamin@example.com',
     '+54 15 2456 9652', 3600, 'Corrientes', 'Av. 7 N° 74 Local 96'),
    ('33254973403', 'Victoria Juan Martin Gomez', 'mcabrera@example.net',
     '+54 9 3618 2662', 5300, 'Resistencia', 'Calle Pte. Perón N° 265'),
    ('33350364078', 'Santiago Nicolas Tomàs Gimenez', 'catalina34@example.com',
     '+54 9 3194 5056', 5400, 'Paraná', 'Av. San Luis N° 83 Piso 4 Dto. 1'),
    ('20121451752', 'Julia Emilia Perez', 'manuelaguero@example.com',
     '+54 15 2243 4830', 1900, 'La Rioja', 'Avenida Alem N° 955'),
    ('33371453860', 'Sr(a). Mateo Escobar', 'camilo27@example.org',
     '+54 15 2901 4786', 4600, 'Paraná', 'Diagonal Rawson N° 153')
]

_budgets = [
    # number, name, date, phone, email, address, additional_discount, client—cuit-cuil
    (105201, "Municipalidad de Concordia", datetime.datetime(
        2023, 8, 12), "",  "", "Concordia (3200), Argentina", 0, ""),
    (105202, "Julia Emilia Perez", datetime.datetime(
        2023, 8, 15), "",  "", "Bolivar 23, Colón, Entre Ríos", 0, "20121451752"),
    (105203, "Municipalidad de Concordia", datetime.datetime(
        2023, 8, 23), "",  "", "Concordia (3200), Argentina", 0, ""),
    (105204, "Federico", datetime.datetime(2023, 8, 23),
     "",  "", "Concordia (3200), Argentina", 0, ""),
]

_budget_items = [
    # product_id, budget_id, quantity, unit_price, sales_category_id, description, fraction_level
    ('APM0007', 105201, 3, 579, 2, 'PELOTA METAL 12 MM', 2),
    ('APM1006', 105201, 22, 377, 2,
     'PLASTICO METALIZADO CAPUCHON 10 MM C/PUNTOS X 500 GRS.', 1),
    ('ATP0005', 105201, 25, 190, 2, 'TACHA PARA PEGAR 8MM 2000 UNID', 2),
    ('ATP0006', 105201, 14, 480, 2, 'TACHA PARA PEGAR 10X10 2000 UNID', 1),
    ('BPN1017', 105201, 15, 580, 2, 'PIEDRA P/COSER NOLITA OVAL 10X14 MM', 1),
    ('BPV1005', 105201, 17, 516, 1, 'PIEDRA CRISTAL 4MM COLOR # CRYSTAL', 0),
    ('ACR1004', 105202, 6, 218, 3, 'CRUZ CHICA PALITO DORADA', 1),
    ('AFD0069', 105202, 21, 346, 3, 'FUNDICION DIJE CHICO CRUZ C/JESUS Y S. BENITO', 1),
    ('APE0006', 105202, 17, 505, 3, 'PERLA ACRILICA 12 MM', 1),
    ('APM1006', 105202, 18, 585, 1,
     'PLASTICO METALIZADO CAPUCHON 10 MM C/PUNTOS X 500 GRS.', 2),
    ('ATP0005', 105202, 18, 614, 1, 'TACHA PARA PEGAR 8MM 2000 UNID', 1),
    ('AFD0069', 105203, 24, 541, 2, 'FUNDICION DIJE CHICO CRUZ C/JESUS Y S. BENITO', 2),
    ('APE0006', 105203, 24, 174, 2, 'PERLA ACRILICA 12 MM', 0),
    ('ATP0006', 105203, 19, 251, 2, 'TACHA PARA PEGAR 10X10 2000 UNID', 1),
    ('MCD1004', 105203, 14, 314, 2, 'CIERRE DIENTE PERRO DESMONTABLE X 45 CM', 1),
    ('MCL2002', 105203, 12, 310, 3, 'CORDON DE LUREX CHINO GRUESO', 1),
    ('APA1003', 105204, 4, 238, 2, 'PIEDRA ENGARZADA PICOS', 2),
    ('ATP0006', 105204, 15, 464, 3, 'TACHA PARA PEGAR 10X10 2000 UNID', 0),
    ('BPV1005', 105204, 6, 617, 1, 'PIEDRA CRISTAL 4MM COLOR # CRYSTAL', 2),
    ('MAM0007', 105204, 25, 244, 1, 'CARRETEL METALICO MAQ.', 2),
    ('MGA0102', 105204, 32, 298, 1,
     'GALON 50253 DE LENT CUAD DE 2.5CM 5 HIL. DE LENT.', 1),
]
