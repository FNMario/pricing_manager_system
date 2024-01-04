from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.lang.builder import Builder

Builder.load_file('screens/widgets/messagebox.kv')


class MessageBox(ModalView):
    """ Widget to create message box.

        :parameters:
            `message`: str,
                The message that will be showed by the message box.
            `kind`: str, defaults to 'information',
                Defines the icon it will show. It can be 'error',
                 'information', 'question' or 'warning'.
            `title`: str, defaults to None,
                If None, the title will be the same as 'kind'.
            `buttons`: str | list, defaults to 'ok_cancel',
                It can be a list of strings, or a string in 
                 ['ok_only', 'ok_cancel', 'yes_no_cancel']
            `on_close`: defaults to (lambda answer: None)
                The function that will be called when a button is pressed.
    """

    answer = None
    image_kind = {
        'error': 'assets/icons/error-hexagon.png',
        'information': 'assets/icons/information-circle.png',
        'question': 'assets/icons/interrogation-circle.png',
        'warning': 'assets/icons/warning-triangle.png',
    }
    button_kinds = {
        'ok_only': ["Ok"],
        'ok_cancel': ["Ok", "Cancel"],
        'yes_no_cancel': ["Yes", "No", "Cancel"]
    }

    def __init__(self,
                 message: str,
                 kind: str = 'information',
                 title: str = None,
                 buttons: str | list = 'ok_cancel',
                 on_close=lambda *x: None,
                 **kwargs):
        super(MessageBox, self).__init__()
        if not title:
            self.title = kind[0].upper() + kind[1:]
        else:
            self.title = title
        self.kind = kind
        self.message = message
        if isinstance(buttons, str):
            self.buttons = self.button_kinds[buttons]
        elif isinstance(buttons, list):
            self.buttons = buttons
        self.on_close = on_close
        self.build()
        self.open()

    def build(self):
        self.ids.lbl_title.text = self.title
        self.ids.lbl_message.text = self.message
        self.ids.icon_image.source = self.image_kind[self.kind]

        def callback(instance):
            self.answer = instance.text
            self.dismiss()
            self.on_close(self.answer)

        for button in self.buttons:
            btn = Button(text=button)
            btn.bind(on_press=callback)
            self.ids.buttons_layout.add_widget(btn)
