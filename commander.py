# Сторонние библиотеки
import pymysql.cursors

# Перечисления команд, режимов
from command_enum import Command
from mode_enum import Mode

# Рабочие модули для переводчика
from directions.translator.yandex_translate import Translator
from directions.translator.transcription import Transcription
from directions.translator.context import Context
from directions.translator.meaning import Meaning
from directions.translator.etymology import Etymology
from directions.mysql.sql import MySQL

# Files
import vk_api
from directions.files.files import Files
from vk_api.upload import VkUpload

# Рабочие модули общего назначения
from directions.help.help import Help

# Config
from config import yandex_translate_api
from config import vk_api_token


class Commander:

	def __init__(self, user_id, group_id, vk_api, session):

		# Текущий, предыдущий режимы
		self.now_mode = Mode.default
		self.last_mode = Mode.default

		self.last_command = None

		# Для запомминания ответов пользователя
		self.last_ans = None

		# Работа с переводом
		self.translator = Translator(yandex_translate_api)

		# Работа с БД
		self.requestDB = None

		# Работа с файлами
		self.requestFile = None

		# Параметры VK API от сервера для текущего пользователя
		self.vk_token = vk_api_token
		self.user_id = user_id
		self.vk_api = vk_api
		self.vk_session = session
		self.group_id = group_id

	@staticmethod
	def get_connection():
		connection = pymysql.connect(host='localhost',
									 user='root',
									 password='1',
									 db='VK_bot_ticket_creator',
									 charset = 'utf8mb4',
									 cursorclass = pymysql.cursors.DictCursor)
		return connection

	# Смена режима / смена мода
	def change_mode(self, to_mode):
		"""
		Меняет режим приема команд
		:param to_mode: Измененный мод
		"""
		self.last_mode = self.now_mode
		self.now_mode = to_mode

		self.last_ans = None

	def input(self, msg):
		"""
		Функция принимающая сообщения пользователя
		:param msg: Сообщение
		:return: Ответ пользователю, отправившему сообщение
		"""

		# Проверка на команду смены мода
		if msg.startswith("/"):
			for mode in Mode:
				if msg[1::] in mode.value:
					self.change_mode(mode)
					return "Режим изменен на " + self.now_mode.value[0]
			return "Неизвестный мод " + msg[1::]

		# Режим получения ответа
		if self.now_mode == Mode.get_answer:
			self.last_ans = msg
			self.now_mode = self.last_mode
			return "Ok!"

		# Проверка режима и действие по режиму --------------------------------

		# стандартный режим
		if self.now_mode == Mode.default:

			if msg not in Command:
				# MySQL.add_to_database(self, msg)
				# add = MySQL.select_from_database(self, msg)
				# print("add ---------------------------")
				# print(add)
				return "Не понял вопроса."

		# действие справки
		if self.now_mode == Mode.help:
			cmd = Help.get_help(self, msg)
			return cmd

		# действие справки
		if self.now_mode == Mode.database:
			if self.requestDB is None:
				self.requestDB = msg
				if self.requestDB == Command.select_in_database.value[0]:
					return "Напишите информацию, которую требуется извлечь из БД:\n " \
						   "Поиск ведется по сообщениямы.\n" \
						   "Для отображения всех данных введите [all|всё|все записи|все данные]"
				if self.requestDB == Command.add_in_database.value[0]:
					return "Напишите информацию, которую требуется добавить в БД в формате [mode message]:"
				else:
					return "Выбранная операция не возможна"
			elif self.requestDB == Command.add_in_database.value[0] or self.requestDB == Command.select_in_database.value[0]:
				self.requestDB += " " + msg
				msg = self.requestDB
				self.requestDB = None
				return MySQL.get_database(self, msg)

		# действие работа с файлами
		if self.now_mode == Mode.files:
			if self.requestFile is None:
				self.requestFile = msg
				if self.requestFile == Command.get_document_file.value[0]:
					return "Укажите название файла:"
				if self.requestFile == Command.get_video_file.value[0]:
					return "Укажите название видеофайла:"
				if self.requestFile == Command.get_audio_file.value[0]:
					return "Укажите название аудиофайла:"
				if self.requestFile == Command.get_searcher_info.value[0]:
					return "Давай я за тебя еще гуглить буду, ага:"
				if self.requestFile == Command.download_files.value[0]:
					return "Загрузите файлы:"
				else:
					return "Выбранная операция не возможна"
			elif self.requestFile == Command.get_document_file.value[0] \
					or self.requestFile == Command.get_video_file.value[0]\
					or self.requestFile == Command.get_audio_file.value[0]\
					or self.requestFile == Command.get_searcher_info.value[0]\
					or self.requestFile == Command.download_files.value[0]:

				self.requestFile += " " + msg
				msg = self.requestFile
				self.requestFile = None
				return Files.files(self, msg)

		return "Команда не распознана!"
