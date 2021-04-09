import requests
from bs4 import BeautifulSoup
from .yandex_translate import Translator

# Config
from config import yandex_translate_api

class Meaning:
    @staticmethod
    def get_meaning(msg) -> list:
        # try:
        #     http = "https://dictionary.cambridge.org/ru/словарь/английский/" + msg
        #     html = BeautifulSoup(requests.get(http).text, "html.parser")
        #     meaning_html = html.select('.def.ddef_d.db')
        #     meaning = meaning_html[0].getText()
        #     print(meaning)
        #     return meaning
        # except:
        #     return "Не удалось найти слово"

        http = "https://dictionary.cambridge.org/ru/словарь/английский/" + msg
        html = BeautifulSoup(requests.get(http).text, "html.parser")
        # meaning_html = html.find_all("ddef_h")
        meaning_html = html.select(".def.ddef_d.db")

        response = "Значения слова (на английском):\n"
        for i, tag in enumerate(meaning_html):
            response += str(i) + ") " + str(tag.text) + "\n"

        response += "\n\nЗначения слова (перевод на русский):\n"
        it = 0
        for i, tag in enumerate(meaning_html):
            translator = Translator(yandex_translate_api)
            print("text = " + str(tag.text))
            it+=1
            try:
                text_ru = translator.translate_to_ru(str(tag.text))
                response += str(it) + ") " + str(text_ru)
            except:
                it-=1
                continue

        return response