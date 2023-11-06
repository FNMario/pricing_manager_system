import logging
from screens.widgets.messagebox import MessageBox
from datetime import datetime as dt

import datetime
import random


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

def get_products_for_sale(product: str = None, local_code: str = None) -> list[str]:
    products = [
        ('AAC0001', 'ARGOLLA PARA CARTERA 45MM', '100.0 UC '),
        ('AAL0001', 'ALAMBRE DE ALPACA 0.5 (5.5 MTS)', '500.0 G10'),
        ('AAL0002', 'ALAMBRE DE ALPAKA 0.6 (4 MTS)', '500.0 G10'),
        ('AAL0003', 'ALAMBRE DE ALPAKA 0.7 (3 MTS)', '500.0 G10'),
        ('AAL0004', 'ALAMBRE DE ALPAKA 0.8(2.25 MTS)', '500.0 G10'),
        ('AAL0005', 'ALAMBRE DE ALPAKA 1.0 (1.5 MTS)', '500.0 G10'),
        ('AAL0006', 'ALAMBRE DE ALPAKA 1.2 (0.65 MTS)', '500.0 G10'),
        ('AAL0007', 'ALAMBRE DE ALPAKA 1/2 CAÑA 2X1 (0.70 MTS)', '500.0 G10'),
        ('AAL0008', 'ALAMBRE DE ALPAKA 1/2 CAÑA 3X1 ( MTS)', '500.0 G10'),
        ('AAL0009', 'ALAMBRE ALUMINIO 1 MM (4.35 MTS)', '500.0 G10'),
        ('AAL0010', 'ALAMBRE ALUMINIO 1.25 MM (2.9 MTS)', '500.0 G10'),
        ('AAL0011', 'ALAMBRE ALUMINIO 1.5 MM (2.1 MTS)', '500.0 G10'),
        ('AAL0012', 'ALAMBRE ALUMINIO 2 MM (1.23 MTS)', '500.0 G10'),
        ('AAL0013', 'ALAMBRE ALUMINIO 2.5 MM (0.75 MTS)', '500.0 G10'),
        ('AAL0014', 'ALAMBRE DE BRONCE 0.5 (5.5 MTS)', '500.0 G10'),
        ('AAL0015', 'ALAMBRE DE BRONCE 0.6 (4 MTS)', '500.0 G10'),
        ('AAL0016', 'ALAMBRE DE BRONCE 0.7 (3 MTS)', '500.0 G10'),
        ('AAL0017', 'ALAMBRE DE BRONCE 0.8 (2.25 MTS)', '500.0 G10'),
        ('AAL0018', 'ALAMBRE DE BRONCE 1.0 (1.5 MTS)', '500.0 G10'),
        ('AAL0019', 'ALAMBRE FORRADO DE ARBORISTERIA NEG-BCO-VERDE NRO23 (3.8MTS EN 10GRS)', '500.0 G10'),
        ('AAM0002', 'ARGOLLA METAL COMUN 4 MM NIKEL-BRONCE', '500.0 G10'),
        ('AAM0003', 'ARGOLLA METAL COMUN 6 MM NIKEL-BRONCE', '500.0 G10'),
        ('AAM0006', 'ARGOLLA METAL COMUN 8 MM NIKEL-BRONCE', '500.0 G10'),
        ('AAM0007', 'ARGOLLA METAL COMUN 10 MM NIKEL-BRONCE', '500.0 G10'),
        ('AAM0009', 'ARGOLLA METAL COMUN 12 MM NIKEL-BRONCE', '500.0 G10'),
        ('AAM0013', 'ARGOLLA METAL COMUN 16 MM NIKEL-BRONCE', '500.0 G10'),
        ('AAM0015', 'ARGOLLA METAL COMUN 18 MM NIKEL-BRONCE', '500.0 G10'),
        ('AAM0017', 'ARGOLLA METAL COMUN 20 MM NIKEL-BRONCE', '500.0 G10'),
        ('AAM0019', 'ARGOLLA METAL COMUN 25 MM NIKEL-BRONCE', '500.0 G10'),
        ('AAM0021', 'ARGOLLA METAL COMUN 30 MM NIKEL-BRONCE', '500.0 G10'),
    ]
    if not product:
        products = products[20:24]
    return products


def get_products(**kwargs) -> list:
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


def save_ivas(ivas: list) -> bool:
    if not ivas:
        return False
    global _ivas
    _ivas = ivas
    return True


def get_dollars() -> list:
    global _dollars
    dollar_now = get_dollar_price()
    return [dollar_now] + _dollars


def save_dollars(dollars: list) -> bool:
    if not dollars:
        return False
    global _dollars
    _dollars = dollars
    return True


def get_suppliers() -> dict:
    global _suppliers
    return _suppliers


def save_suppliers(suppliers: list) -> bool:
    if not suppliers:
        return False
    global _suppliers
    _suppliers = suppliers
    return True


def get_fractions() -> dict:
    global _fractions
    return _fractions


def save_fractions(fractions: list) -> bool:
    if not fractions:
        return False
    global _fractions
    _fractions = fractions
    return True


def get_sections() -> dict:
    global _sections
    return _sections


def save_sections(sections: list) -> bool:
    if not sections:
        return False
    global _sections
    _sections = sections
    return True


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


def calculate_prices_from_costs(quantity: float, unit: str, cost: float, surcharge: float = None, surcharge_level: int = None):

    if surcharge is not None:
        if surcharge >= 0 and surcharge < 1.70:
            surcharge_level = 0
        elif surcharge < 2.00:
            surcharge_level = 1
        elif surcharge < 2.20:
            surcharge_level = 2
        elif surcharge < 2.50:
            surcharge_level = 3
        elif surcharge < 3.50:
            surcharge_level = 4
        elif surcharge < 4.50:
            surcharge_level = 5
        elif surcharge >= 4.50:
            surcharge_level = 6
        else:
            raise (ValueError("Surcharge must be bigger than 0"))
    elif surcharge_level is not None:
        if surcharge_level not in range(7):
            raise ValueError(
                "Invalid surcharge level. It must be between 0 and 6")
    else:
        raise (TypeError("You must provide surcharge or surcharge_level"))

    unitary_cost = cost / quantity

    try:
        fractions_list = get_fractions()
        fraction_index = [_[1].strip() for _ in fractions_list].index(unit.strip())
        fractions = list(fractions_list[fraction_index][4:7])
        str_unit = fractions_list[fraction_index][3]
    except ValueError:
        fractions = [1, -1, 0]
        str_unit = unit

    price = unitary_cost * surcharge

    prices = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]

    for category in range(3):
        for fraction in range(3):
            if fractions[fraction] == -1:
                fractions[fraction] = quantity
            prices[fraction][category] = price * fractions[fraction] * \
                _apply_discount(surcharge_level, fraction, category)

    return prices, fractions, str_unit


def round_prices(prices):
    return [[round(price_0), round(price_1), round(price_2)] for price_0, price_1, price_2 in prices]


def get_product_prices(product_code):
    prices = [
        [250.25, 242, 225],
        [4000, 3970, 3925],
        [7000, 6800, 6500],
    ]
    quantities = [
        "LOS 25 GRAMOS",
        "LOS 500 GRAMOS",
        "EL kILO"
    ]
    date = dt.strftime(
        dt.today() - datetime.timedelta(random.randrange(40)), "%d/%m/%Y")
    return round_prices(prices), quantities, date


def format_numeric_economy(price: float):
    return f'{price:,.2f}'.replace(',', chr(0x2009))


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
