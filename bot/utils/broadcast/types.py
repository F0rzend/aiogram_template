from string import Template
from typing import Union, List, Dict

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply

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
