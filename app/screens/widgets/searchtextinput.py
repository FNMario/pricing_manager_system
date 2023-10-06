from kivy.uix.textinput import TextInput
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty

Builder.load_file('screens/widgets/searchtextinput.kv')


class SearchTextInput(TextInput):
    table = ObjectProperty(None)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):

        if keycode[1] in ('up', 'down') and self.table:
            try:
                self.table._on_keyboard_down(window, keycode, text, modifiers)
                return False
            except Exception as e:
                print(e)
        return super(SearchTextInput, self).keyboard_on_key_down(window, keycode, text, modifiers)
