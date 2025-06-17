from enum import Enum


class TextStyle(Enum):
    UNDERLINE = 'underline'
    STRONG = 'strong'
    EMPHASIZED = 'emphasized'
    MONOSPACED = 'monospaced'
    LINK = 'link'
    STRIKETHROUGH = 'strikethrough'
    USER_MENTION = 'user_mention'
    HEADING = 'heading'
    HIGHLIGHTED = 'highlighted'