from string import Template
from typing import Dict, List, Union

from aiogram.types import (ForceReply, InlineKeyboardMarkup,
                           ReplyKeyboardMarkup, ReplyKeyboardRemove)

ChatIdType = Union[int, str]
ChatIdsType = Union[List[ChatIdType], ChatIdType]
ChatsType = Union[ChatIdsType, List[Dict]]
TextType = Union[Template, str]
MarkupType = Union[
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply,
    None,
]
