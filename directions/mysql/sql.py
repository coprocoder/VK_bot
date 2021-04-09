import requests
import pymysql.cursors
from command_enum import Command
from mode_enum import Mode

class MySQL:

    @staticmethod
    def get_database(self, msg) -> list:
        if msg.startswith(Command.add_in_database.value[0]):
            msg = msg[7::]
            ls = msg.split(" ")
            if(len(ls)!=2):
                return "Введите данные в заданном формате"
            else:
                return MySQL.add_to_database(self, ls[0], ls[1])
        if msg.startswith(Command.select_in_database.value[0]):
            msg = msg[7::]
            return MySQL.select_from_database(self, msg)
        if msg in Command.main_menu.value:
            return self.change_mode(Mode.default)

    @staticmethod
    def add_to_database(self, mode, msg):
        # Создаем новую сессию
        connection = self.get_connection()
        # Будем получать информацию от сюда
        cursor = connection.cursor()
        # Наш запрос
        sql = "INSERT INTO messages (mode, user_id, group_id, message) VALUES (%s, %s, %s, %s)"
        # Выполняем наш запрос и вставляем свои значения
        cursor.execute(sql, (mode, 456, 987, msg))
        # Делаем коммит
        connection.commit()
        # Закрываем подключение
        connection.close()
        # Возвращаем результат
        return "Запись добавлена в базу данных"

    @staticmethod
    def select_from_database(self, msg):
        connection = self.get_connection()
        cursor = connection.cursor()
        print("msg -------------------------")
        print(msg)
        if msg in Command.select_all.value:
            sql = "SELECT * FROM vk_bot_ticket_creator.messages"
            cursor.execute(sql)
        else:
            sql = "SELECT * FROM vk_bot_ticket_creator.messages WHERE LOCATE(TRIM(LOWER(%s)), mode) > 0 or LOCATE(TRIM(LOWER(%s)), message) > 0"
            cursor.execute(sql, (msg, msg))

        # Получаем запрашиваемые данных и заносим их в переменные
        response = ""
        for i, line in enumerate(cursor):
            response += str(line['user_id']) + ") " + str(line['message']) + '\n'
        # Проверяем точно ли есть такая запись
        if cursor.fetchall() == ():
            response = 'Таких сообщений нет'
        connection.close()

        return response