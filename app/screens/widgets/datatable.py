from kivy.properties import ListProperty, BooleanProperty, NumericProperty, ColorProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.lang.builder import Builder
from kivy.core.window import Window

import logging

Builder.load_file('screens/widgets/datatable.kv')


class Header(Label):

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos) and not touch.is_mouse_scrolling:
            root = self.parent.parent
            index = root.header.index(self.text)
            raw_items_dict = {row: item for row, item in enumerate(root.items)}
            sorted_items_dict = dict(
                sorted(raw_items_dict.items(), key=lambda x: x[1][index]))
            root.row = 0
            root.body_layout.clear_widgets()
            for row, item in sorted_items_dict.items():
                root.add_dato(item, row)


class Row(Label):
    background = BooleanProperty(False)
    row = NumericProperty()
    selected_color = ColorProperty([.2, .8, .2, 1])
    default_color = ColorProperty([1, 1, 1, 1])

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos) and not touch.is_mouse_scrolling:
            self.parent.parent.parent.selected_row = self.row


class DataTable(BoxLayout):
    header = ListProperty(["Title"])
    hint_sizes = ListProperty([])
    checkboxes = BooleanProperty(False)
    items = ListProperty([])
    row = 0
    selected_row = NumericProperty(0)

    def __init__(self, **kwargs):
        super(DataTable, self).__init__(**kwargs)

        self.bind(header=self.update_table)
        self.bind(items=self.update_table)
        self.bind(selected_row=self.update_selected_row)

        self.register_event_type('on_selected_row')

        # Initialize the table
        self.update_table()

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'up':
            self.selected_row = max(0, self.selected_row - 1)
        elif keycode[1] == 'down':
            self.selected_row = min(len(self.items) - 1, self.selected_row + 1)
        return True

    def update_table(self, *args):
        self.clear_widgets()
        self.row = 0
        self.header_layout = GridLayout()
        self.header_layout.cols = len(self.header) + int(self.checkboxes)
        self.body_layout = GridLayout(size_hint_y=None)
        self.body_layout.bind(minimum_height=self.body_layout.setter('height'))
        self.body_layout.cols = self.header_layout.cols

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

            self.header_layout.add_widget(checkbox_all)

        try:
            assert(len(self.hint_sizes) == len(self.header))
        except:
            self.hint_sizes = self.hint_sizes + [1] * (len(self.header) - len(self.hint_sizes))

        for hint_size, header_item in zip(self.hint_sizes, self.header):
            header_label = Header(
                text=header_item,
                bold=True,
                size_hint_y=None,
                size_hint_x=hint_size,
                height=30,
            )
            self.header_layout.add_widget(header_label)

        self.header_layout.size_hint_y = None
        try:
            self.header_layout.height = self.header_layout.children[0].height
        except:
            pass
        self.add_widget(self.header_layout)

        for item in self.items:
            self.add_dato(item)

        scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
        )
        scroll.add_widget(self.body_layout)
        self.add_widget(scroll)

        self.selected_row = 0
        self.update_selected_row()

    def add_dato(self, dato: tuple, row: list = None):
        # assert len(dato) == self.cols, f"len(dato):{len(dato)}, != {self.cols}"

        # add checkbox
        if self.checkboxes:
            self.body_layout.add_widget(
                CheckBox(
                    size_hint=(None, None),
                    height=20,
                    width=30
                )
            )
        for hint_size, item in zip(self.hint_sizes, dato):
            self.body_layout.add_widget(
                Row(
                    row=row if row else self.row,
                    text=str(item),
                    background=bool(self.row % 2 == 1),
                    size_hint_x=hint_size,
                    size_hint_y=None,
                    height=20,
                )
            )

        self.row += 1

    def update_selected_row(self, *args):
        for child in self.body_layout.children:
            if isinstance(child, Row):
                if child.row == self.selected_row:
                    child.color = child.selected_color
                    child.bold = True
                else:
                    child.color = child.default_color
                    child.bold = False
        self.dispatch('on_selected_row')

    def on_selected_row(self, *args):
        pass
