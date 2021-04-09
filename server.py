import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from commander import Commander
from command_enum import Command
from mode_enum import Mode

class Server:

    def __init__(self, api_token, group_id, server_name: str="Empty"):

        # Даем серверу имя
        self.server_name = server_name
        self.group_id = group_id

        # Для Long Poll
        self.vk = vk_api.VkApi(token=api_token)

        # Для использоания Long Poll API
        self.longpoll = VkLongPoll(self.vk, wait=30, group_id=group_id)

        # Для вызова методов vk_api
        self.vk_api = self.vk.get_api()

        # Словарь дял каждого отдельного пользователя
        self.users = {}

        self.msg = ""
        self.mode = ""
        self.keyboard_file = ""

    def send_msg(self, send_id, message):
        """
        Отправка сообщения через метод messages.send
        :param send_id: vk id пользователя, который получит сообщение
        :param message: содержимое отправляемого письма
        :return: None
        """

        return self.vk_api.messages.send(peer_id=send_id,
                                         message=message,
                                         random_id=random.randint(0, 2048),
                                         keyboard=open(self.keyboard_file, "r", encoding="UTF-8").read())

    def start(self):
        for event in self.longpoll.listen():   # Слушаем сервер
            if event.type == VkEventType.MESSAGE_NEW:
                print('Новое сообщение:')
                self.msg = event.text

                if self.msg.startswith("/"):
                    for mode in Mode:
                        if self.msg[1::] in mode.value:
                            self.mode = mode

                if event.from_me:
                    print('От меня для: ', end='')
                elif event.to_me:
                    if event.user_id not in self.users:
                        self.users[event.user_id] = Commander(event.user_id, self.group_id, self.vk_api, self.vk)
                    if event.type == VkEventType.MESSAGE_NEW:
                        self.msg = self.users[event.user_id].input(event.text)

                        if self.mode == Mode.help:
                            self.keyboard_file = "keyboards/help.json"
                        elif self.mode == Mode.translate:
                            self.keyboard_file = "keyboards/translator.json"
                        elif self.mode == Mode.database:
                            self.keyboard_file = "keyboards/database.json"
                        elif self.mode == Mode.files:
                            self.keyboard_file = "keyboards/files.json"
                        else:
                            self.keyboard_file = "keyboards/default.json"

                        self.send_msg(event.user_id, self.msg)

                    print('Для меня от: ', end='')

                if event.from_user:
                    print(event.user_id)
                elif event.from_chat:
                    print(event.user_id, 'в беседе', event.chat_id)
                elif event.from_group:
                    print('группы', event.group_id)

                print('Текст: ', event.text)

            elif event.type == VkEventType.USER_TYPING:
                print('Печатает ', end='')

                if event.from_user:
                    print(event.user_id)
                elif event.from_group:
                    print('администратор группы', event.group_id)

            elif event.type == VkEventType.USER_TYPING_IN_CHAT:
                print('Печатает ', event.user_id, 'в беседе', event.chat_id)

            elif event.type == VkEventType.USER_ONLINE:
                print('Пользователь', event.user_id, 'онлайн', event.platform)

            elif event.type == VkEventType.USER_OFFLINE:
                print('Пользователь', event.user_id, 'оффлайн', event.offline_type)

            else:
                print(event.type, event.raw[1:])