from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty, BooleanProperty, NumericProperty, ColorProperty
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.lang.builder import Builder

Builder.load_file('screens/widgets/datatable.kv')


class Header(Label):
    pass


class Row(Label):
    background = BooleanProperty(False)
    row = NumericProperty()
    selected_color = ColorProperty([.2, .8, .2, 1])
    default_color = ColorProperty([1, 1, 1, 1])

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.parent.update_selected_row(self.row)


class DataTable(GridLayout):
    header = ListProperty(["prueba"])
    hint_sizes = ListProperty([])
    checkboxes = BooleanProperty(False)
    items = ListProperty([])
    row = 0
    selected_row = NumericProperty(0)

    def __init__(self, **kwargs):
        super(DataTable, self).__init__(**kwargs)

        self.bind(header=self.update_table)
        self.bind(items=self.update_table)

        self.register_event_type('on_selected_row')

        # Initialize the table
        self.update_table()

    def update_table(self, *args):
        self.clear_widgets()
        self.row = 0
        self.cols = len(self.header) + int(self.checkboxes)

        # add checkbox "all"
        if self.checkboxes:
            checkbox_all = CheckBox(
                size_hint=(None, None),
                height=30,
                width=30
            )

            def on_checkbox_active(checkbox, value):
                for child in self.children:
                    if isinstance(child, CheckBox):
                        child.active = checkbox.active
            checkbox_all.bind(active=on_checkbox_active)

            self.add_widget(checkbox_all)

        for hint_size, header_item in zip(self.hint_sizes, self.header):
            header_label = Header(
                text=header_item,
                bold=True,
                size_hint_y=None,
                size_hint_x=hint_size,
                height=30,
            )
            self.add_widget(header_label)

        for item in self.items:
            self.add_dato(item)

        if len(self.items) > 0:
            self.selected_row = 0
        else:
            self.selected_row = 0

    def add_dato(self, dato: tuple):
        # assert len(dato) == self.cols, f"len(dato):{len(dato)}, != {self.cols}"

        # add checkbox
        if self.checkboxes:
            self.add_widget(
                CheckBox(
                    size_hint=(None, None),
                    height=20,
                    width=30
                )
            )
        for hint_size, item in zip(self.hint_sizes, dato):
            self.add_widget(
                Row(
                    row=self.row,
                    text=str(item),
                    background=bool(self.row % 2 == 1),
                    size_hint_x=hint_size,
                    size_hint_y=None,
                    height=20,
                )
            )

        self.row += 1

    def update_selected_row(self, selected_row):
        self.selected_row = selected_row
        for child in self.children:
            if isinstance(child, Row):
                if child.row == selected_row:
                    child.color = child.selected_color
                    child.bold = True
                else:
                    child.color = child.default_color
                    child.bold = False
        self.dispatch('on_selected_row')

    def on_selected_row(self, *args):
        pass
