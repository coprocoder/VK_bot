import requests
from bs4 import BeautifulSoup
from .yandex_translate import Translator

# Config
from config import yandex_translate_api

class Context:
    @staticmethod
    def get_context(msg) -> list:

        http = "https://dictionary.cambridge.org/ru/словарь/английский/" + msg
        html = BeautifulSoup(requests.get(http).text, "html.parser")
        response = "Ответ:\n"
        for i, def_block in enumerate(html.find_all(class_="def-block ddef_block")):

            title = def_block.find_next(class_="def ddef_d db")
            # print("\ntitle")
            # print(title)
            # print("\ntetle text")
            # print(title.text)

            examples_block = def_block.find_next(class_="def-body ddef_b")
            # print("\nexamples")
            # print(examples_block)
            # print("\nexamples text")
            # print(examples_block.text)

            response += "\n\n" + str(i+1) + ") " + title.text + "\n"
            for example in examples_block:
                try:
                    # ex = example #.find_next(class_="examp dexamp")
                    # print("example")
                    # print(ex.text)
                    response += "--" + example.text + "\n"
                except:
                    continue




        '''lst = html.find_all(class_="def-block ddef_block")
        # Первый результат
        response = ""
        text = lst[0].text.strip()
        count = text.count(":") - 1
        text = text.replace(":", ":\n   * ", count)
        count = text.count(".") - 1
        text = text.replace(".", "\n   * ", count)
        response += "0) " + text

        # Все последующие результаты
        for i, items in enumerate(lst):
            if i!=len(lst)-1:
                try:
                    data = items.find_next_sibling().text
                    data = data.replace("Больше примеров\n", "")
                    count = data.count(":") - 1
                    data = data.replace(":", ":\n   * ", count)
                    count = data.count(".") - 1
                    data = data.replace(".", "\n   * ", count)
                    response += "\n" + str(i+1) + ") " + data.strip()
                    print(type(data))
                    print(data)
                except:
                    data = ""'''

        # response = "Контекст слова (на английском):\n"
        # for i, tag in enumerate(meaning_html):
        #     response += str(i) + ") " + str(tag.text) + "\n"
        #
        # response += "\n\nКонтекст слова (перевод на русский):\n"
        # for i, tag in enumerate(meaning_html):
        #     translator = Translator(yandex_translate_api)
        #     text_ru = translator.translate_to_ru(tag.text)
        #     text = text_ru.split("Переведено сервисом")
        #     response += str(i) + ") " + str(text[0])
        # return response

        return response