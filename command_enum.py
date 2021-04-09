from enum import Enum


class Command(Enum):

    main_menu = ["default", "главное меню"]

    """ help_commands """
    help_commands = ["commands", "комманды"]
    help_modes = ["modes", "режимы"]

    """ database_commands """
    # add_in_database = ["insert", "вставить"]
    # select_in_database = ["select", "найти"]
    # select_all = ["all", "*", "всё", "все записи", "все данные"]

    """ files_commands """
    get_audio_file = ["audio", "аудио"]
    get_video_file = ["video", "видео"]
    get_document_file = ["docs", "документ"]
    get_searcher_info = ["searcher", "поисковик"]
    download_files = ["upload", "загрузить"]




'''    """ translate """
    translate = ["/translate", "перевод"]

    """ meaning """
    meaning = ["/meaning", "значение"]

    """ transcription """
    transcription = ["/transcription", "транскрипция"]

    """ context """
    context = ["/context", "контекст"]

    """ etymology """
    etymology = ["/etymology", "этимология"]
'''

