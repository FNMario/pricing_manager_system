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


class _Header(Label):

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos) and not touch.is_mouse_scrolling:
            root = self.parent.parent
            if root.items:
                index = root.header.index(self.text)
                raw_items_dict = {row: item for row,
                                  item in enumerate(root.items)}
                sorted_items_dict = dict(
                    sorted(raw_items_dict.items(), key=lambda x: str(x[1][index])))
                root._row = 0
                root._rows_index.clear()
                root._checkboxes.clear()
                root.body_layout.clear_widgets()
                for row, item in sorted_items_dict.items():
                    root.add_item(item, row)
                root.selected_row = root._rows_index[0]


class _Row(Label):
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
    show_checkboxes = BooleanProperty(False)
    checkbox_active_default = BooleanProperty(False)
    items = ListProperty([])
    selected_row = NumericProperty(0)

    def __init__(self, **kwargs):
        super(DataTable, self).__init__(**kwargs)
        
        self._checkboxes = list()
        self._row = 0
        self._rows_index = list()

        self.bind(header=self.update_header)
        self.bind(items=self.update_body)
        self.bind(selected_row=self.update_selected_row)

        self.register_event_type('on_selected_row')

        # Initialize the table
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'up':
            try:
                index = self._rows_index.index(self.selected_row) - 1
                if index >= 0:
                    self.selected_row = self._rows_index[index]
            except IndexError:
                pass
        elif keycode[1] == 'down':
            try:
                index = self._rows_index.index(self.selected_row) + 1
                self.selected_row = self._rows_index[index]
            except IndexError:
                pass
        return True

    def update_header(self, *args):
        self.clear_widgets()
        self._row = 0
        self._rows_index.clear()
        self._checkboxes.clear()
        self.header_layout = GridLayout(padding=(8, 0))
        self.header_layout.cols = len(self.header) + int(self.show_checkboxes)
        self.body_layout = GridLayout(size_hint_y=None, padding=(8, 0), row_default_height=36)
        self.body_layout.bind(minimum_height=self.body_layout.setter('height'))
        self.body_layout.cols = self.header_layout.cols

        # add checkbox "all"
        if self.show_checkboxes:
            self.checkbox_all = CheckBox(
                size_hint=(None, None),
                height=30,
                width=30,
                active=self.checkbox_active_default
            )

            def on_checkbox_active(checkbox, value):
                for child in self.body_layout.children:
                    if isinstance(child, CheckBox):
                        child.active = checkbox.active
            self.checkbox_all.bind(active=on_checkbox_active)

            self.header_layout.add_widget(self.checkbox_all)

        if len(self.hint_sizes) < len(self.header):
            self.hint_sizes = self.hint_sizes + \
                [1] * (len(self.header) - len(self.hint_sizes))

        for hint_size, header_item in zip(self.hint_sizes, self.header):
            header_label = _Header(
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

        self.scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            scroll_type=['bars', 'content'],
            bar_width=8,
            effect_cls="ScrollEffect"
        )
        self.scroll.add_widget(self.body_layout)
        self.add_widget(self.scroll)

    def update_body(self, *args):
        self.update_header()

        for item in self.items:
            self.add_item(item)

        self.selected_row = 0
        self.update_selected_row()

    def add_item(self, item: tuple, row: list = None):
        assert len(
            item) + int(self.show_checkboxes) == self.body_layout.cols, f"program_error: len(item):{len(item)} != {self.body_layout.cols - int(self.show_checkboxes)}"

        # add checkbox
        if self.show_checkboxes:
            checkbox = CheckBox(
                # size_hint=(None, None),
                # height=20,
                size_hint_x=None,
                width=30,
                active=self.checkbox_all.active
            )
            self._checkboxes.append(checkbox)
            self.body_layout.add_widget(checkbox)

        if row == None:
            row = self._row

        for hint_size, item in zip(self.hint_sizes, item):
            _value = _Row(
                row=row,
                text=str(item),
                background=bool(self._row % 2 == 1),
                size_hint_x=hint_size,
                # size_hint_y=None,
                # height=20,
            )
            self.body_layout.add_widget(_value)
        self._rows_index.append(row)
        self._row += 1

    def update_selected_row(self, *args):
        for child in self.body_layout.children:
            if isinstance(child, _Row):
                if child.row == self.selected_row:
                    child.color = child.selected_color
                    child.bold = True
                    if self.scroll.height < self.body_layout.height:
                        self.scroll.scroll_to(child)
                else:
                    child.color = child.default_color
                    child.bold = False
                # if child.texture_size[1] > 20:
                #     self.body_layout.rows_minimum[child.row] = child.texture_size[1]
                #     logging.debug(f'datatable.py: {child.text_size} {child.texture_size} {child.size}col: {child.text}')
                # # if child.texture_size[0] > child.size[0]:
                # #     logging.debug(f'datatable.py: {child.text_size} {child.texture_size} {child.size}col: {child.text}')
        self.dispatch('on_selected_row')

    def on_selected_row(self, *args):
        pass

    def switch_checkbox_state(self, row):
        if self._checkboxes and row in range(self._row):
            checkbox = self._checkboxes[self._rows_index.index(row)]
            checkbox.active = not checkbox.active
            return True
        return False

    def get_checkboxes_state(self):
        if self._checkboxes:
            order = (_ for _ in self._rows_index)
            return [checkbox.active for checkbox in sorted(self._checkboxes, key=lambda _: next(order))]

        else:
            return []

    def get_checked_rows(self):
        if self._checkboxes:
            return [row for i, row in enumerate(self._rows_index) if self._checkboxes[i].state == 'down']
        else:
            return []
