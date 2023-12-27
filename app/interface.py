import datetime
from datetime import datetime as dt
from screens.widgets.messagebox import MessageBox
import logging


class DatabaseError(Exception):
    pass

# Users


def login(username, password):
    # Call the database function to fetch user data
    return True


def create_new_user(username, password):
    # Call the database function to insert a new user
    return (username, password)


def update_user_password(username, old_pass, new_pass):
    return (username, new_pass)


# Products

def get_products_for_sale(product: str = None, local_code: str = None, supplier_code: str = None) -> list[str]:
    global _list_of_products_for_sale
    if not product:
        products = _list_of_products_for_sale[20:24]
    else:
        products = _list_of_products_for_sale
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
        'from_date': from_date,
        'to_date': to_date
    }
    global _list_of_products_with_costs

    products = _list_of_products_with_costs  # db.get_complete_items(**kwargs)
    return products


def get_last_code(base: str) -> str:
    return base + '158'


def save_product(data: dict):
    units = {f[1]: f[0] for f in get_fractions()}
    sections = {key: value for value, key in get_sections()}
    suppliers = {_[1]: _[0] for _ in get_suppliers()}

    new_product = {
        'description': data['product'],
        'code_id': data['local_code'],
        'quantity': data['quantity'],
        'fraction_id': units[data['unit']],
        'section_id': sections[data['section']]
    }

    new_cost = {
        'product_id': data['local_code'],
        'supplier_id': suppliers[data['supplier']],
        'supplier_code': data['supplier_code'],
        'cost': data['cost'],
        'surcharge': data['surcharge'],
        'date': data['date'],
        'dollar_price': data['dollar']
    }

    # old_product = db.get_product(code_id=new_product['code_id'])

    # if not old_product:
    #     db.add_product(new_product)
    #     db.add_cost(new_cost)
    #     return

    # if old_product['quantity'] != new_product['quantity'] or old_product['fraction_id'] != new_product['fraction_id']:
    #     raise DatabaseError("quantity and/or fraction doesn't match with product code. Try new code or replace it")
    # else:
    #     db.alter_product(new_product)

    #     old_cost = db.get_cost(product_id=cost['product_id'], supplier_id=cost['supplier_id'])

    #     if not old_cost:
    #         db.add_cost(new_cost)
    #     else:
    #         db.alter_cost(new_cost)


def delete_product(data: dict, all_costs: bool = False):

    def answer_clicked(answer):
        print(f'Perform action? {answer}')
        if answer == "Delete all" or answer == "Delete":
            try:
                # db.delete_cost(product_id=data['local_code'])
                # db.delete_product(code_id=data['local_code'])
                pass
            except Exception as e:
                logging.error(e)
        elif answer == "Only this one":
            try:
                # db.delete_cost(product_id=data['local_code'], supplier_id=cost['supplier_id'])
                pass
            except Exception as e:
                logging.error(e)
            pass
        else:
            logging.error("Canceled by the user")

    costs = [
        (21, 'AAM0002', 12, None, 335.8117, datetime.date(2019, 8, 16), 2.53, 60.0),
        (22, 'AAM0002', 12, None, 133.0, datetime.date(2019, 8, 16), 3.0, 60.0),
        (23, 'AAM0002', 21, None, 455.0, datetime.date(2019, 8, 16), 2.8, 58.5)
    ]  # db.get_cost(product_id=data['local_code'])
    if len(costs) > 1:
        message = f"There are {len(costs)} suppliers for this products:"
        suppliers = {_[0]: _[1] for _ in get_suppliers()}
        for cost in costs:
            message += f"\n- Supplier: {suppliers[cost[2]]:0>15}, Cost: ${cost[4]} "
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
    global _ivas
    return _ivas


def save_ivas(iva: float, row: int = -1) -> bool:
    global _ivas
    if 0 < row and row < len(_ivas):
        _ivas[row] = float(iva)
        return True
    else:
        _ivas.append(iva)
        return True
    return False


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
    global _suppliers
    return _suppliers


def save_supplier(supplier: dict) -> bool:
    global _suppliers
    assert 'name' in supplier, "program_error."
    assert supplier['name'], "Name cannot be empty"
    assert 'phone' in supplier, "program_error."
    assert 'email' in supplier, "program_error."
    assert 'address' in supplier, "program_error."
    if 'id' in supplier:
        assert supplier['id'], "id cannot be empty"
        id = int(supplier.pop('id'))
        # db.save_in_table(table='suppliers', id=id, data=supplier)
        _suppliers[id] = (
            id,
            supplier['name'],
            supplier['phone'],
            supplier['email'],
            supplier['address'],
        )
        return True
    else:
        # db.save_in_table(table='suppliers', data=supplier)
        _suppliers.append((
            _suppliers[-1][0] + 1,
            supplier['name'],
            supplier['phone'],
            supplier['email'],
            supplier['address'],
        ))
        return True
    return False


def get_fractions() -> list[tuple]:
    global _fractions
    return _fractions


def save_fraction(fraction: dict) -> bool:
    global _fractions
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
    if 'id' in fraction:
        assert fraction['id'], "id cannot be empty"
        id = int(fraction.pop('id'))
        # db.save_in_table(table='fractions', id=id, data=fraction)
        _fractions[id-1] = (
            id,
            fraction['name'],
            fraction['description'],
            fraction['unit'],
            fraction['fraction_1'],
            fraction['fraction_2'],
            fraction['fraction_3'],
        )
        return True
    else:
        # db.save_in_table(table='fractions', data=fraction)
        _fractions.append((
            _fractions[-1][0] + 1,
            fraction['name'],
            fraction['description'],
            fraction['unit'],
            fraction['fraction_1'],
            fraction['fraction_2'],
            fraction['fraction_3'],
        ))
        return True
    return False


def get_sections() -> list[tuple]:
    global _sections
    return _sections


def save_section(section: dict) -> bool:
    global _sections
    assert 'name' in section, "program_error."
    assert section['name'], "Name cannot be empty"
    if 'id' in section:
        assert section['id'], "id cannot be empty"
        id = int(section.pop('id'))
        # db.save_in_table(table='sections', id=id, data=section)
        _sections[id] = (
            id,
            section['name'],
        )
        return True
    else:
        # db.save_in_table(table='sections', data=section)
        _sections.append((
            _sections[-1][0] + 1,
            section['name'],
        ))
        return True
    return False


def get_clients() -> list[tuple]:
    global _clients
    return _clients


def get_client(cuit_cuil: str) -> list[tuple]:
    clients = get_clients()
    return [client for client in clients if client[0].replace('-', '') == cuit_cuil.replace('-', '')]


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
    assert 'cp' in client, "program_error."
    client.update(
        {
            'cuit_cuil': client['cuit_cuil'].replace('-', ''),
            'cp': int(client['cp']),
            'name': client['name'].title()
        }
    )
    try:
        # db.save_client(data=client)
        item = (
            client['cuitcuil'],
            client['name'],
            client['email'],
            client['phone'],
            client['cp'],
            client['city'],
            client['address']
        )
        client_cuits = [_[0] for _ in get_clients()]
        if client['cuit_cuil'] in client_cuits:
            index = client_cuits.index(client['cuit_cuil'])
            _clients[index] = item
            return True
        else:
            _clients.append(item)
    except Exception as e:
        logging.error(e)
        return False


def get_budgets(budget_number: int, name: str, from_date, to_date) -> list[tuple]:
    global _budgets
    return _budgets


def get_budget_items(budget_number: int) -> list[tuple]:
    # items = db.get_budget_items(budget_number)
    # categories= {1:"V", 2:"D", 3:"M"}
    # for item in items:
    #     item = (
    #         item[0],
    #         item[1],
    #         item[2],
    #         categories[item[3]],
    #         item[4],
    #         item[5],
    #     )
    # return items
    global _budget_items
    categories= {1:"V", 2:"D", 3:"M"}
    items_to_return = list()
    for item in _budget_items:
        if item[1] == budget_number:
            items_to_return.append((
                item[0],
                item[2],
                item[3],
                categories[item[4]],
                item[5],
                item[6]
            ))
    return items_to_return

# product_id, ~budget_id, quantity, unit_price, sales_category_id, description, fraction_level



def save_budget(budget_data: dict, items: list) -> bool:
    has_cuit = budget_data['cuit_cuil'] != ""
    has_name = budget_data['name'] != ""
    has_budget_number = budget_data['budget_number'] > 0
    has_items = len(items) > 0
    assert has_budget_number, "Program error: no valid budget number."
    assert has_cuit or has_name, "Budget must have a cuit and/or a name."
    assert has_items, "Budget must have at least one product."
    budget_data.update({
        'id': budget_data['budget_number'],
        'client_cuit_cuil': budget_data['cuit_cuil']
    })
    logging.info('Budget: Budget saved!')
    # saved_items = db.get_budget_items(budget_number=budget_data['budget_number'])
    # items_to_drop = list()
    # categories = {"V":1, "D":2, "M":3}
    # for item in items:
    #     item[2] = categories[item[2]]
    # for item in saved_items:
    #     if item[1:] in items:
    #         items.remove(item[1:])
    #     else:
    #         items_to_drop.append(item)
                
    # db.drop_items(items=items_to_drop)
    # db.save_items(items=items)
    # db.save_budget(budget_data=budget_data)



def get_tables_to_print_names(section: str, name: str = None) -> list[str]:
    # db.get_tables_to_print_names(section, name)
    tables = [('usesrs',), ('orders',)]
    return tables


def get_table_to_print_data(section: str, name: str) -> (list[str], list[str]):
    delete_this = [('ADS0004', True), ('APA1003', True), ('APM1006', True), ('MAM0007', True), ('MBR0007', True),
                   ('chk_client_1_fraction_1', False), ('chk_fraction_1', False), ('chk_client_1_fraction_2',  False), ('chk_fraction_2', False), ('chk_date', False)]
    data = delete_this  # db.get_tables_to_print_data(name)
    rows = [item for item, is_row in data if is_row]
    columns = [item for item, is_row in data if not is_row]
    return rows, columns


def add_tables_to_print_name(section: str, name: str):
    pass


def save_tables_to_print_name(section: str, old_name: str, new_name: str):
    pass


def save_table_to_print_data(items_code, headers):
    pass


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
        fractions = list(fractions_list[fraction_index][4:7])
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

    quantity, unit, price, discount_level, date = (
        1005, "G10", 1044.5058, 3, "2020-02-06")  # db.get_product_prices(product_code)

    prices, fractions, str_unit = calculate_prices(
        quantity=quantity, unit=unit, price=price, discount_level=discount_level)

    quantities = [f"{_} {str_unit}" for _ in fractions]

    return round_prices(prices), quantities, date


def format_numeric_economy(price: float, show_currency_symbol: bool = False, currency_symbol: str = "$") -> str:
    if show_currency_symbol:
        return f"{currency_symbol}{chr(0x2009)}{price:,.2f}".replace(",", chr(0x2009))
    else:
        return f"{price:,.2f}".replace(",", chr(0x2009))


# External

def get_date():
    return dt.strftime(dt.today(), '%d/%m/%Y')


def get_dollar_price():
    return 835


# Listas temporales

_dollars = [800, 900]

_ivas = [10.5, 21.]

_suppliers = [
    (0, "OTROS", "", "", ""),
    (1, "A. MANIA", "", "", ""),
    (2, "ALOE", "", "", ""),
    (3, "BISANS", "", "", ""),
    (4, "BISCUIT", "", "", ""),
    (5, "COCO FIL", "", "", ""),
    (6, "COTINA", "", "", ""),
    (7, "EL BOLSERO", "", "", ""),
    (8, "FERRETERIA", "", "", ""),
    (9, "GATUVIA", "", "", ""),
    (10, "IKORSO", "", "", ""),
    (11, "JR", "", "", ""),
    (12, "KAIZEN", "", "", ""),
    (13, "KRAMIR", "", "", ""),
    (14, "KREY", "", "", ""),
    (15, "LAINO", "", "", ""),
    (16, "MARIBELLA", "", "", ""),
    (17, "MEIR GROUP", "", "", ""),
    (18, "MERMIL", "", "", ""),
    (19, "MONICA", "", "", ""),
    (20, "MOSTACILLA", "", "", ""),
    (21, "MUNDO A", "", "", ""),
    (22, "NEPTUNO", "", "", ""),
    (23, "OSCAR", "", "", ""),
    (24, "PALACIO", "", "", ""),
    (25, "PALAIS", "", "", ""),
    (26, "PAW", "", "", ""),
    (27, "PEGAMIL", "", "", ""),
    (28, "SUSESSO", "", "", ""),
    (29, "TELGOPOR", "", "", ""),
    (30, "TURCO", "", "", ""),
    (31, "UNIPOX", "", "", ""),
    (32, "SANTERIA BELEN", "", "", ""),
    (33, "SARQUIS Y SEPAG", "", "", ""),
    (34, "MODA SHOP", "", "", ""),
    (35, "PUNTO BIJOU", "", "", ""),
    (36, "GERERDO", "", "", ""),
    (37, "GASTON", "", "", ""),
]

_sections = [
    (0, "ARMADOR"),
    (1, "BRILLO"),
    (2, "MERCERIA"),
    (3, "LIBRERIA"),
    (4, "ELECTRONICA"),
    (5, "PEGAMENTOS"),
    (6, "PLUMAS"),
    (7, "AMAZONA"),
    (8, "BOA"),
    (9, "ESPIGADA"),
    (10, "FAISAN CEBRA"),
    (11, "FAISAN LADY"),
    (12, "FLEX"),
    (13, "RABO GA"),
    (14, "INSTRUMENTO"),
]

_fractions = [
    (1, "U  ", "Unidades: x1u/Paquete Cerrado",
        "Unidades", 1, -1, 0),
    (2, "UC ", "Unidades: x1u/x100u/", "Unidades", 1, 100, 500),
    (3, "G10", "Gramos: x10g/x100g/x500g", "Gramos", 10, 100, 500),
    (4, "G25", "Gramos: x25g/x100g/x500g", "Gramos", 25, 100, 500),
    (5, "M  ", "Metros: x1m/Paquete Cerrado",
        "Metros", 1, -1, 0),
    (6, "MC ", "Metros: x1m/x10m", "Metros", 1, 10, 0),
    (7, "Y  ", "Yardas: x1m/Paquete Cerrado",
        "Yardas", 1.0936, -1, 0),
    (8, "T  ", "Tiras: x1/x10", "Yardas", 1, 10, 0),
]


_list_of_products_with_costs = [
    ('ALAMBRE DE ALPAKA 1/2 CAÑA 2X1 (0.70 MTS)', 'AAL0007', 'BISCUIT', None,
     500.0, 'G10', 570.0, 2.51, 'ARMADOR', datetime.date(2019, 8, 16), 60.0, None),
    ('ALAMBRE DE ALPAKA 1/2 CAÑA 3X1 ( MTS)', 'AAL0008', 'BISCUIT', None, 500.0,
     'G10', 570.0, 2.51, 'ARMADOR', datetime.date(2019, 8, 16), 60.0, None),
    ('BUZIO GRANDE MARRON  X 500GR.', 'ABU0008', 'MOSTACILLA', 'AS27261',
     270.0, 'UC ', 0.0, 0.0, 'ARMADOR', datetime.date(2019, 8, 16), 58.5, None),
    ('BUZIO MARRON POR 500 GRS. (80 UNID. APROX.)', 'ABU0009', 'MOSTACILLA', None,
     80.0, 'UC ', 0.0, 2.5, 'ARMADOR', datetime.date(2019, 8, 16), 58.5, None),
    ('CASCABEL 16MM MULTICOLOR', 'ACA4006', 'ALOE', None, 200.0, 'UC ',
     0.0, 0.0, 'ARMADOR', datetime.date(2019, 8, 16), 58.5, None),
    ('CAPUCHON DORADOS 10MM', 'ACC0006', 'JR', None, 1000.0, 'UC ',
     1596.0, 2.5, 'ARMADOR', datetime.date(2019, 8, 16), 60.0, None),
    ('CADENA CHICA COD T110-35', 'ACM0008', 'JR', 'T110-35', 10.0, 'M  ',
     57.323, 2.55, 'ARMADOR', datetime.date(2019, 8, 16), 60.0, None),
    ('CADENA SHANEL PLANO 1.2 MM', 'ACM0062', 'KREY', '1532195-96', 10.0,
     'M  ', 0.0, 2.5, 'ARMADOR', datetime.date(2019, 8, 16), 60.0, None),
    ('CADENA SHANEL PLANO 1.0 MM', 'ACM0064', 'KREY', '1532197-98', 10.0,
     'M  ', 0.0, 2.5, 'ARMADOR', datetime.date(2019, 8, 16), 60.0, None),
    ('CADENA SHANEL TRIPLE PLANA GRANDE JR', 'ACM0092', 'JR', 'TS20-110/2DC',
     10.0, 'M  ', 399.0, 2.5, 'ARMADOR', datetime.date(2019, 8, 16), 60.0, None),
    ('FUNDICION', 'AFA0000', 'JR', None, 250.0, 'G10', 399.0,
     2.5, 'ARMADOR', datetime.date(2019, 8, 16), 60.0, None),
    ('FILIGRANA BUHO', 'AFI0001', 'JR', 'HU-9051', 10.0, 'U  ',
     399.0, 2.35, 'ARMADOR', datetime.date(2019, 8, 16), 60.0, None),
    ('FUNDICION PORTA DIJE Nº 22', 'AFP0010', 'JR', None, 89.0, 'U  ',
     285.285, 2.5, 'ARMADOR', datetime.date(2019, 8, 16), 60.0, None),
    ('FUNDICION SEPARADOR Nº 03 C', 'AFS1011', 'JR', 'W-454', 52.0, 'U  ',
     228.095, 2.5, 'ARMADOR', datetime.date(2019, 8, 16), 60.0, None),
    ('FUNDICION SEPARADOR Nº 28', 'AFS1055', 'JR', 'W-325', 61.0, 'U  ',
     342.475, 2.5, 'ARMADOR', datetime.date(2019, 8, 16), 60.0, None),
    ('MOSQUETON P/LLAVERO REDONDEADO 33 MM', 'AGM0018', 'IKORSO', 'SWK20-N', 100.0,
     'UC ', 1425.0, 2.5, 'ARMADOR', datetime.date(2018, 10, 18), 37.5, None),
    ('OJOS TURCOS ENGANCHADOS X 10MTS.', 'AOT1002', 'JR', None, 10.0,
     'M  ', 2394.0, 2.5, 'ARMADOR', datetime.date(2019, 8, 16), 60.0, None),
    ('PIEDRA ACRILICA POR KG.', 'APA0001', 'ALOE', '379', 500.0, 'G10',
     171.3635, 2.5, 'ARMADOR', datetime.date(2019, 8, 16), 58.5, None),
    ('PIEDRA ACRILICA POR KG.', 'APA0001', 'ALOE', '415', 500.0, 'G10',
     171.3635, 2.5, 'ARMADOR', datetime.date(2019, 8, 16), 58.5, None),
    ('PIEDRA ACRILICA FORMA. CHUPETE. MAMADERA. ETC.', 'APA0002', 'JR', None,
     500.0, 'G10', 399.0, 3.0, 'ARMADOR', datetime.date(2019, 8, 16), 60.0, None),
    ('PIEDRA ACRILICA CAIREL GOTA PLANA  DE COLORES METALIZADOS', 'APA0004', 'JR',
     'S1785', 500.0, 'G10', 399.0, 3.0, 'ARMADOR', datetime.date(2019, 8, 16), 60.0, None),
    ('PERLA ACRILICA 3 MM', 'APE0001', 'PALACIO', None, 500.0, 'G10',
     0.0, 2.5, 'ARMADOR', datetime.date(2019, 8, 16), 58.5, None),
    ('PERLA ACRILICA 4 MM', 'APE0002', 'PALACIO', None, 500.0, 'G10',
     0.0, 2.5, 'ARMADOR', datetime.date(2019, 8, 16), 58.5, None),
    ('PERLA ACRILICA 6 MM', 'APE0003', 'PALACIO', None, 500.0, 'G10',
     0.0, 2.5, 'ARMADOR', datetime.date(2019, 8, 16), 58.5, None),
    ('PERLA PLASTICA 8 MM', 'APE0004', 'PALACIO', None, 500.0, 'G10',
     0.0, 2.5, 'ARMADOR', datetime.date(2019, 8, 16), 58.5, None),
    ('PERLA PLASTTICA Nº10 X 500GRS.', 'APE0005', 'PALACIO', None, 500.0,
     'G10', 0.0, 2.5, 'ARMADOR', datetime.date(2019, 8, 16), 58.5, None),
    ('PERLA JAPONESA POR KG', 'APE1005', 'PAW', None, 500.0, 'G10',
     456.0, 2.6, 'ARMADOR', datetime.date(2019, 8, 16), 60.0, None),
    ('PERLA JAPONESA CIEGA POR KG 8MM', 'APE1006', 'PAW', None, 500.0,
     'G10', 456.0, 2.6, 'ARMADOR', datetime.date(2019, 8, 16), 60.0, None),
    ('PELOTA METAL 4 MM', 'APM0002', 'JR', 'NIK X KG.', 6000.0, 'UC ',
     1197.0, 2.5, 'ARMADOR', datetime.date(2019, 8, 24), 57.0, None),
    ('PELOTA METAL 4 MM', 'APM0002', 'JR', 'NIK X KG.', 6000.0, 'UC ',
     798.0, 2.5, 'ARMADOR', datetime.date(2019, 8, 16), 60.0, None)
]

_list_of_products_for_sale = [
    ('ACC1003', 'CORDON 8 MM RASTA COSIDO',
     '10 Metros', 'ARMADOR', '\\Image11.bmp', None),
    ('ACM0048', 'CADENA MALLA PLANA 8.0', '10 Metros', 'ARMADOR', None, '1382454'),
    ('ACR1004', 'CRUZ CHICA PALITO DORADA',
     '200 Unidades', 'ARMADOR', None, '17214-51'),
    ('ACR2002', 'CENTRO DE ROSARIO MEDIANAS BR Y NIK.',
     '100 Unidades', 'ARMADOR', None, ' 13211-53'),
    ('ADS0004', 'DIJE C/STRASS DIJE DE LA PAZ',
     '20 Unidades', 'ARMADOR', None, None),
    ('AFD0061', 'FUNDICION DIJE CHICO ESTRELLA LISA 25 MM',
     '287 Unidades', 'ARMADOR', None, None),
    ('AFD0069', 'FUNDICION DIJE CHICO CRUZ C/JESUS Y S. BENITO',
     '375 Unidades', 'ARMADOR', None, 'K3093'),
    ('AKR0022', 'MEDALLA ESPIRITU SANTO METAL SOLO 40MM',
     '10 Unidades', 'ARMADOR', '\\20170517_091439.jpg', None),
    ('AKR0026', 'MEDALLA ITALIANA OVAL 16X22MM',
     '10 Unidades', 'ARMADOR', None, None),
    ('APA1003', 'PIEDRA ENGARZADA PICOS', '10 Unidades',
     'ARMADOR', '\\20170514_193235.jpg', None),
    ('APE0006', 'PERLA ACRILICA 12 MM', '500 Gramos', 'ARMADOR', None, None),
    ('APF1003', 'PELOTA FILIGRANADA 8 MM', '2000 Unidades',
     'ARMADOR', None, '10130-NIK,10130-DOR,POR KG.'),
    ('APM0006', 'PELOTA METAL 10 MM', '1000 Unidades', 'ARMADOR',
     None, 'NIK,11007-520 PL,11007-53 NK,NIK X KG.,LISA'),
    ('APM0007', 'PELOTA METAL 12 MM', '500 Unidades',
     'ARMADOR', None, 'LISA,NIK X KG.'),
    ('APM1006', 'PLASTICO METALIZADO CAPUCHON 10 MM C/PUNTOS X 500 GRS.',
     '824 Unidades', 'ARMADOR', None, 'W1237'),
    ('ATP0005', 'TACHA PARA PEGAR 8MM 2000 UNID',
     '2000 Unidades', 'ARMADOR', None, None),
    ('ATP0006', 'TACHA PARA PEGAR 10X10 2000 UNID',
     '2000 Unidades', 'ARMADOR', None, None),
    ('BPL1009', 'PIEDRA P/COSER LASER OVAL 30X40 MM ALOE',
     '50 Unidades', 'BRILLO', None, 'C30X40'),
    ('BPN1017', 'PIEDRA P/COSER NOLITA OVAL 10X14 MM',
     '1000 Unidades', 'BRILLO', None, 'A3205  S$U 10.81 X 20.5'),
    ('BPP0003', 'PIEDRAS P/PEGAR 7MM X 5000U.',
     '5000 Unidades', 'BRILLO', None, None),
    ('BPV1005', 'PIEDRA CRISTAL 4MM COLOR # CRYSTAL',
     '144 Unidades', 'BRILLO', None, None),
    ('LGE0002', 'GOMA EVA CON BRILLO', '10 Unidades', 'LIBRERIA', None, None),
    ('LPG0028', 'ECOLE X 9 GRS.', '10 Unidades', 'LIBRERIA', None, None),
    ('LPG1001', 'SUPRABOND ADHESIVO DE CONTACTO TRANSPARENTE X 25ML.',
     '6 Unidades', 'LIBRERIA', None, None),
    ('MAM0007', 'CARRETEL METALICO MAQ.',
     '10 Unidades', 'MERCERIA', None, '100060'),
    ('MAM0008', 'AGUJA CANASTITA CHINA', '12 Unidades', 'MERCERIA', None, '040045'),
    ('MAP0303', 'APLIQUES DE STRASS TERMOAHDESIVO A6515',
     '10 Unidades', 'MERCERIA', None, 'A6515 2D A $30'),
    ('MBR0007', 'OJAL BRONCE BHYN N°20', '144 Unidades', 'MERCERIA', None, None),
    ('MCB0002', 'CIERRE BRONCE YKK 12 CM',
     '12 Unidades', 'MERCERIA', None, '11-0034'),
    ('MCB0006', 'CIERRE BRONCE YKK 20 CM',
     '12 Unidades', 'MERCERIA', None, '11-0038'),
    ('MCD0013', 'CIERRE DESMONTABLE 6 MM X 85 CM',
     '12 Unidades', 'MERCERIA', None, None),
    ('MCD1004', 'CIERRE DIENTE PERRO DESMONTABLE X 45 CM',
     '12 Unidades', 'MERCERIA', None, '120091'),
    ('MCL1021', 'CINTA LUREX CHINA 20 MM X 50YDS',
     '10 Unidades', 'MERCERIA', None, None),
    ('MCL2002', 'CORDON DE LUREX CHINO GRUESO',
     '10 Metros', 'MERCERIA', None, None),
    ('MFL0013', 'GALON  DE FLECO', '42 Metros', 'MERCERIA', None, '1526292'),
    ('MGA0102', 'GALON 50253 DE LENT CUAD DE 2.5CM 5 HIL. DE LENT.',
     '18.28 Metros', 'BRILLO', None, '50253'),
    ('MGA0172', 'GALON CON PIEDRA GAT A8-1007-1',
     '10 Yardas', 'BRILLO', None, 'A8-1007-1'),
    ('MTE4002', 'TELA LAME BONDEADO XMTS', '10 Metros', 'MERCERIA', None, None),
    ('PRG0004', 'RABO DE GALLO BLANCO 30/35CM AL',
     '1000 Gramos', 'RABO GA', None, 'PLCH71001'),
]


_clients = [
    ("20123456789", "Estefanía Maria Gonzales", "estefania.maria.gonzales@example.com",
     "1234567890", 1234, "Buenos Aires", "123 Calle Falsa"),
    ("23234567890", "Juan Carlos Rodriguez", "juan.carlos.rodriguez@example.com",
     "2345678901", 2345, "Córdoba", "456 Calle Falsa"),
    ("27345678901", "María Fernández", "maria.fernandez@example.com", "3456789012",
     3456, "Rosario", "789 Calle Falsa"),
    ("30456789012", "Carlos Alberto Gómez", "carlos.alberto.gomez@example.com",
     "4567890123", 4567, "Mendoza", "1011 Calle Falsa"),
    ("33567890123", "Ana Laura Pérez", "ana.laura.perez@example.com",
     "5678901234", 5678, "La Plata", "1213 Calle Falsa"),
    ("20678901234", "Luis Alberto Sánchez", "luis.alberto.sanchez@example.com",
     "6789012345", 6789, "San Miguel", "1415 Calle Falsa")
]

_budgets = [
    # number, name, date, phone, email, address, additional_discount, client—cuit-cuil
    (105201, "Municipalidad de Concordia", datetime.datetime(
        2023, 8, 12), "",  "", "Concordia (3200), Argentina", 0, ""),
    (105202, "Estefanía Gonzales", datetime.datetime(
        2023, 8, 15), "",  "", "Bolivar 23, Colón, Entre Ríos", 0, "20123456789"),
    (105203, "Municipalidad de Concordia", datetime.datetime(
        2023, 8, 23), "",  "", "Concordia (3200), Argentina", 0, ""),
    (105204, "Federico", datetime.datetime(2023, 8, 23),
     "",  "", "Concordia (3200), Argentina", 0, ""),
]

_budget_items = [
    # product_id, budget_id, quantity, unit_price, sales_category_id, description, fraction_level
    ('APM0007', 105201, 3, 579, 2, 'PELOTA METAL 12 MM', 2),
    ('APM1006', 105201, 22, 377, 2, 'PLASTICO METALIZADO CAPUCHON 10 MM C/PUNTOS X 500 GRS.', 1),
    ('ATP0005', 105201, 25, 190, 2, 'TACHA PARA PEGAR 8MM 2000 UNID', 2),
    ('ATP0006', 105201, 14, 480, 2, 'TACHA PARA PEGAR 10X10 2000 UNID', 1),
    ('BPN1017', 105201, 15, 580, 2, 'PIEDRA P/COSER NOLITA OVAL 10X14 MM', 1),
    ('BPV1005', 105201, 17, 516, 1, 'PIEDRA CRISTAL 4MM COLOR # CRYSTAL', 0),
    ('ACR1004', 105202, 6, 218, 3, 'CRUZ CHICA PALITO DORADA', 1),
    ('AFD0069', 105202, 21, 346, 3, 'FUNDICION DIJE CHICO CRUZ C/JESUS Y S. BENITO', 1),
    ('APE0006', 105202, 17, 505, 3, 'PERLA ACRILICA 12 MM', 1),
    ('APM1006', 105202, 18, 585, 1, 'PLASTICO METALIZADO CAPUCHON 10 MM C/PUNTOS X 500 GRS.', 2),
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
    ('MGA0102', 105204, 32, 298, 1, 'GALON 50253 DE LENT CUAD DE 2.5CM 5 HIL. DE LENT.', 1),
]
