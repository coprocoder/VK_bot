from enum import Enum


class Mode(Enum):
    default = ["Обычный режим", "default"]
    translate = ["Режим переводчика", "translate"]
    transcription = ["Режим вывода транскрипции", "transcription"]
    meaning = ["Режим вывода значения", "meaning"]
    context = ["Режим вывода контекста", "context"]
    etymology = ["Режим вывода этимологии", "etymology"]
    help = ["Режим вывода справки", "help"]
    database = ["Режим работы с БД", "database"]
    files = ["Режим работы с файлами", "files"]
    get_answer = ["Режим ввода ответа", "get_answer"]
