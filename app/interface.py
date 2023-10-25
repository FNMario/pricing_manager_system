from datetime import datetime as dt

import datetime
import random


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


def get_products() -> list:
    products = [
        (105, "Auriculares", 25, "Electrónica RST"),
        (106, "Mouse", 30, "Informática UVW"),
        (107, "Teclado", 35, "Informática UVW"),
        (108, "Parlante", 40, "Electrónica RST"),
        (109, "Impresora", 5, "Informática UVW"),
        (110, "Tinta", 10, "Papelería ABC"),
        (111, "Papel", 100, "Papelería ABC"),
        (112, "Marcador", 50, "Papelería XYZ"),
        (113, "Lámpara", 15, "Electrónica RST"),
        (114, "Reloj", 20, "Joyería OPQ"),
        (115, "Anillo", 10, "Joyería OPQ"),
        (116, "Collar", 15, "Joyería OPQ"),
        (117, "Pulsera", 20, "Joyería OPQ"),
        (118, "Aretes", 25, "Joyería OPQ"),
        (119, "Bolso", 10, "Moda GHI"),
        (120, "Cartera", 15, "Moda GHI"),
        (121, "Zapatos", 20, "Moda GHI"),
        (122, "Camisa", 25, "Moda GHI"),
        (123, "Pantalón", 30, "Moda GHI"),
        (124, "Gorra", 10, "Deportes DEF"),
        (125, "Pelota", 15, "Deportes DEF"),
        (126, "Raqueta", 20, "Deportes DEF"),
        (127, "Bicicleta", 5, "Deportes DEF"),
        (128, "Casco", 10, "Deportes DEF"),
        (129, "Libro", 50, "Librería LMN"),
        (130, "Revista", 100, "Librería LMN"),
        (131, "Periódico", 200, "Librería LMN"),
        (132, "Mapa", 50, "Librería LMN"),
        (133, "Calendario", 100, "Librería LMN"),
        (134, "Chocolate", 50, "Alimentos JKL"),
        (135, "Galletas", 100, "Alimentos JKL"),
        (136, "Café", 25, "Alimentos JKL"),
        (137, "Té", 25, "Alimentos JKL"),
        (138, "Leche", 50, "Alimentos JKL"),
        (139, "Jabón", 100, "Higiene FED"),
        (140, "Shampoo", 50, "Higiene FED"),
        (141, "Crema dental", 75, "Higiene FED"),
        (142, "Desodoran asdf as fasef asef asf asef ase fasf asef as asea fwe fas ase faste", 50, "Higiene FED"),
        (143, "Toalla húmeda", 100, "Higiene FED"),
        (144, "Vino tinto", 25, "Bebidas CBA"),
        (145, "Vino blanco", 25, "Bebidas CBA"),
        (146, "Cerveza", 50, "Bebidas CBA"),
        (147, "Agua mineral", 100, "Bebidas CBA"),
        (148, "Jugo de naranja", 75, "Bebidas CBA"),
        (149, "Arroz blanco", 50, "Granos ZYX"),
        (150, "Arroz integral", 25, "Granos ZYX"),
        (151, "Lentejas", 25, "Granos ZYX"),
        (152, "Garbanzos", 25, "Granos ZYX"),
        (153, "Frijoles negros", 50, "Granos ZYX"),
    ]
    return products


def find_per_product_name(text: str) -> list:
    products = [
        (105, "Auriculares", 25, "Electrónica RST"),
        (106, "Mouse", 30, "Informática UVW"),
        (107, "Teclado", 35, "Informática UVW"),
        (108, "Parlante", 40, "Electrónica RST"),
        (109, "Impresora", 5, "Informática UVW"),
        (110, "Tinta", 10, "Papelería ABC"),
        (111, "Papel", 100, "Papelería ABC"),
        (112, "Marcador", 50, "Papelería XYZ"),
        (113, "Lámpara", 15, "Electrónica RST"),
        (114, "Reloj", 20, "Joyería OPQ"),
        (138, "Leche", 50, "Alimentos JKL"),
        (139, "Jabón", 100, "Higiene FED"),
        (140, "Shampoo", 50, "Higiene FED"),
        (141, "Crema dental", 75, "Higiene FED"),
        (142, "Desodoran asdf as fasef asef asf asef ase fasf asef as asea fwe fas ase faste", 50, "Higiene FED"),
        (143, "Toalla húmeda", 100, "Higiene FED"),
        (144, "Vino tinto", 25, "Bebidas CBA"),
        (145, "Vino blanco", 25, "Bebidas CBA"),
        (146, "Cerveza", 50, "Bebidas CBA"),
    ]
    return products


def find_per_local_code(text: str) -> list:
    products = [
        (147, "Agua mineral", 100, "Bebidas CBA"),
        (148, "Jugo de naranja", 75, "Bebidas CBA"),
        (149, "Arroz blanco", 50, "Granos ZYX"),
        (150, "Arroz integral", 25, "Granos ZYX"),
    ]
    return products


def find_per_suppliers_code(text: str) -> list:
    products = [
        (114, "Reloj", 20, "Joyería OPQ"),
    ]
    return products


def get_last_code(base: str) -> str:
    return base + '158'


def alter_product(**kwargs):
    print(kwargs)


def alter_cost(**kwargs):
    print(kwargs)


def save_product(data: dict):
    units = {f[1]: f[0] for f in get_fractions()}
    sections = get_sections()
    suppliers = get_suppliers()

    # db.alter_product(
    alter_product(
        product=data['product'],
        local_code=data['local_code'],
        quantity=data['quantity'],
        unit=units[data['unit']],
        section=sections[data['section']]
    )

    # db.alter_cost(
    alter_cost(
        product_id=data['local_code'],
        supplier=suppliers[data['supplier']],
        supplier_code=data['supplier_code'],
        cost=data['cost'],
        surcharge=data['surcharge'],
        date=data['date'],
        dollar=data['dollar']
    )


def add_product(product: dict):
    pass


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
    return _dollars


def save_dollars(dollars: list) -> bool:
    if not dollars:
        return False
    global _dollars
    _dollars = dollars
    return True


def get_suppliers() -> dict:
    global _suppliers
    return {key: value for value, key in enumerate(_suppliers)}


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
    return {key: value for value, key in enumerate(_sections)}


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

    if surcharge:
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
    elif surcharge_level:
        if surcharge_level not in range(7):
            raise ValueError(
                "Invalid surcharge level. It must be between 0 and 6")
    else:
        raise (TypeError("You must provide surcharge or surcharge_level"))

    unitary_cost = cost / quantity

    fractions = [0, 0, 0]
    if unit == "U" or unit == "M":
        fractions[0] = 1
        fractions[1] = quantity
        fractions[2] = 0
    elif unit == "UC":
        fractions[0] = 1
        fractions[1] = 100
        fractions[2] = 500
    elif unit == "MC":
        fractions[0] = 1
        fractions[1] = 10
        fractions[2] = 0
    elif unit == "T":
        fractions[0] = 1
        fractions[1] = 10
        fractions[2] = 0
    elif unit == "G10":
        fractions[0] = 10
        fractions[1] = 100
        fractions[2] = 500
    elif unit == "G25":
        fractions[0] = 25
        fractions[1] = 100
        fractions[2] = 500
    elif unit == "Y":
        fractions[0] = 1 / 0.914
        fractions[1] = quantity
        fractions[2] = 0
    else:
        fractions[0] = 1
        fractions[1] = quantity
        fractions[2] = 0

    price = unitary_cost * surcharge

    prices = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]

    for category in range(3):
        for fraction in range(3):
            prices[fraction][category] = price * fractions[fraction] * \
                _apply_discount(surcharge_level, fraction, category)

    return prices, fractions


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


def number_category(convert: str | int) -> int | str:

    number_category = [
        ("VENTAS", 0),
        ("DESCUENTOS", 1),
        ("MAYORISTA", 2),
    ]
    result = [n for c, n in number_category if c == convert]
    if result:
        return result[0]
    result = [c for c, n in number_category if n == convert]
    if result:
        return result[0]
    raise ValueError(f"Invalid input.\n Valid inputs: {number_category}")


# External

def get_date():
    return dt.strftime(dt.today(), '%d/%m/%Y')


def get_dollar_price():
    global _dollars
    return _dollars[0]


# Listas temporales

_dollars = [805, 385]

_ivas = [10.5, 21.]

_suppliers = [
    "OTROS",
    "A. MANIA",
    "ALOE",
    "BISANS",
    "BISCUIT",
    "COCO FIL",
    "COTINA",
    "EL BOLSERO",
    "FERRETERIA",
    "GATUVIA",
    "IKORSO",
    "JR",
    "KAIZEN",
    "KRAMIR",
    "KREY",
    "LAINO",
    "MARIBELLA",
    "MEIR GROUP",
    "MERMIL",
    "MONICA",
    "MOSTACILLA",
    "MUNDO A",
    "NEPTUNO",
    "OSCAR",
    "PALACIO",
    "PALAIS",
    "PAW",
    "PEGAMIL",
    "SUSESSO",
    "TELGOPOR",
    "TURCO",
    "UNIPOX",
    "SANTERIA BELEN",
    "SARQUIS Y SEPAG",
    "MODA SHOP",
    "PUNTO BIJOU",
    "GERERDO",
    "GASTON",
]

_sections = [
    "ARMADOR",
    "BRILLO",
    "MERCERIA",
    "LIBRERIA",
    "ELECTRONICA",
    "PEGAMENTOS",
    "PLUMAS",
    "AMAZONA",
    "BOA",
    "ESPIGADA",
    "FAISAN CEBRA",
    "FAISAN LADY",
    "FLEX",
    "RABO GA",
    "INSTRUMENTO",
]

_fractions = [
    (1, "U", "Unidades: x1u/Paquete Cerrado",
        "Unidades", "x1u", "Paquete Cerrado", ""),
    (2, "UC", "Unidades: x1u/x100u/", "Unidades", "x1u", "x100u", "x500u"),
    (3, "G10", "Gramos: x10g/x100g/x500g", "Gramos", "x10g", "x100g", "x500g"),
    (4, "G25", "Gramos: x25g/x100g/x500g", "Gramos", "x25g", "x100g", "x500g"),
    (5, "M", "Metros: x1m/Paquete Cerrado",
        "Metros", "x1m", "Paquete Cerrado", ""),
    (6, "MX", "Metros: x1m/x10m", "Metros", "x1m", "x10m", ""),
    (7, "Y", "Yardas: x1m/Paquete Cerrado",
        "Yardas", "x1m", "Paquete Cerrado", ""),
    (8, "T", "Tiras: x1/x10", "Yardas", "x1", "x10", ""),
]
