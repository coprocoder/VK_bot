import requests
from bs4 import BeautifulSoup
from .yandex_translate import Translator

# Config
from config import yandex_translate_api

class Etymology:
    @staticmethod
    def get_etymology(msg) -> list:

        http = "https://www.etymonline.com/word/" + msg
        html = BeautifulSoup(requests.get(http).text, "html.parser")
        etymology_html = html.select(".word__defination--2q7ZH")
        print(etymology_html)

        response = "Контекст слова (на английском):\n"
        for i, tag in enumerate(etymology_html):
            response += "\n\n" + str(tag.text) + "\n"

        # response += "\n\nКонтекст слова (перевод на русский):\n"
        # for i, tag in enumerate(etymology_html):
        #     translator = Translator(yandex_translate_api)
        #     text_ru = translator.translate_to_ru(tag.text)
        #     text = text_ru.split("Переведено сервисом")
        #     response += str(i) + ") " + str(text[0])

        return response