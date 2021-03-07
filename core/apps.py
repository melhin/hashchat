from django.apps import AppConfig
from core.translator import Translator


class CoreConfig(AppConfig):
    name = 'core'
    translator = Translator()
