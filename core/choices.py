from enum import Enum


class AuthentiationMethod(Enum):
    EMAIL = 'auth.type.email'
    TWITTER = 'auth.type.twitter'


class LanguageChoices(Enum):
    EN = 'en'
    DE = 'de'
