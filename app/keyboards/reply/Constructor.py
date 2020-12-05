from typing import Dict, List, Union

from aiogram.types import KeyboardButton, KeyboardButtonPollType, ReplyKeyboardMarkup

from app.utils.MarkupConstructorCore import MarkupConstructorCore


class ReplyConstructor(MarkupConstructorCore):
    """
        Class for creating reply keyboards

        Usage example:
            class ExampleMarkup(InlineConstructor):
                callback_data = CallbackData('test', 'number')
                def generate(self):
                    schema = [3, 2, 1]
                    actions = [
                        {'text': '1', 'callback_data': self.callback_data.new('1')},
                        {'text': '2', 'callback_data': self.callback_data.new('2')},
                        {'text': '3', 'callback_data': '3'},
                        {'text': '4', 'callback_data': self.callback_data.new('4')},
                        {'text': '5', 'callback_data': (self.callback_data, '5')},
                        {'text': '6', 'callback_data': '6'},
                    ]
                    return self.generate_keyboard(actions, schema)
        """
    aliases = {
        'request_contact':  'contact',
        'request_location': 'location',
        'request_poll':     'poll'
    }
    available_properties = ['text', 'request_contact', 'request_location', 'request_poll']
    properties_amount = 2

    def _replace_aliases(
            self,
            action: Union[str, Dict[str, Union[str, bool, KeyboardButtonPollType]]],
    ):
        super()._replace_aliases(action)

    def _check_properties(
            self,
            action: Union[str, Dict[str, Union[str, bool, KeyboardButtonPollType]]],
    ) -> Dict[str, Union[str, bool]]:
        return super()._check_properties(action)

    def generate_keyboard(
            self,
            actions: List[Union[str, Dict[str, Union[str, bool, KeyboardButtonPollType]]]],
            schema: List[int]
    ) -> ReplyKeyboardMarkup:
        markup = ReplyKeyboardMarkup()
        markup.row_width = max(schema)
        buttons = list()
        for action in actions:
            self._replace_aliases(action)
            button_data = self._check_properties(action)
            buttons.append(KeyboardButton(**button_data))
        markup.keyboard = self.create_keyboard_layout(buttons, schema)
        return markup
