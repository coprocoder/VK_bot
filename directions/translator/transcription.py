import requests
from bs4 import BeautifulSoup

class Transcription:
    @staticmethod
    def get_transcription(msg) -> list:
        try:
            http = "https://dictionary.cambridge.org/ru/словарь/английский/" + msg
            html = BeautifulSoup(requests.get(http).text, "html.parser")
            trans_html = html.select('.pron.dpron')
            transcription = trans_html[0].getText()
            print(transcription)
            return transcription
        except:
            return "Не удалось найти слово"

        '''http = "https://translate.academic.ru/" + msg + "/en/ru/"
        html = BeautifulSoup(requests.get(http).text, "html.parser")
        meaning_html = html.select('.translate_definition .dic_transcription')
        try:
            transcription = meaning_html[0].getText()
            return transcription
        except:
            content = html.select('.terms-list')
            print("content type")
            print(type(content))
            find = re.search("\[(.*?)\]",content.get_text())
            print("\n\n\nfind = ")
            print(find)
            return "Не удалось найти слово"'''





