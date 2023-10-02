from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
import logging

Builder.load_file('screens/manage_prices_screen.kv')

class ManagePrices(Widget):

    def btn_on_press(self):
        print('button_pressed')

    def check_press(self, instance):
        print(instance)
        print(instance.active)
        
    def search(self,quantity=49):
        lista = [
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
            (133, "Calendario", 100,"Librería LMN"),
            (134,"Chocolate",50,"Alimentos JKL"),
            (135,"Galletas",100,"Alimentos JKL"),
            (136,"Café",25,"Alimentos JKL"),
            (137,"Té",25,"Alimentos JKL"),
            (138,"Leche",50,"Alimentos JKL"),
            (139,"Jabón",100,"Higiene FED"),
            (140,"Shampoo",50,"Higiene FED"),
            (141,"Crema dental",75,"Higiene FED"),
            (142,"Desodoran asdf as fasef asef asf asef ase fasf asef as asea fwe fas ase faste",50,"Higiene FED"),
            (143,"Toalla húmeda",100,"Higiene FED"), 
            (144,"Vino tinto",25,"Bebidas CBA"), 
            (145,"Vino blanco",25,"Bebidas CBA"), 
            (146,"Cerveza",50,"Bebidas CBA"), 
            (147,"Agua mineral",100,"Bebidas CBA"), 
            (148,"Jugo de naranja",75,"Bebidas CBA"), 
            (149,"Arroz blanco",50,"Granos ZYX"), 
            (150,"Arroz integral",25,"Granos ZYX"), 
            (151,"Lentejas",25,"Granos ZYX"), 
            (152,"Garbanzos",25,"Granos ZYX"), 
            (153,"Frijoles negros" ,50 ,"Granos ZYX"), 
        ]
        return lista[:quantity]

    def clean_forms(self, parent):
        for child in parent.children:
            if child.children:
                self.clean_forms(child)
            else:
                if isinstance(child, TextInput): 
                    child.text = ""

    def clean_all(self):
        self.clean_forms(self.ids.form_layout)
        self.ids.tbl_products.items = []
        self.ids.tbl_products.update_table()

class PriceManagerApp(App):
    def build(self):
        Window.clearcolor = (.13, .14, .19, 1)
        return ManagePrices()
