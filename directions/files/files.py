import requests
import json

from command_enum import Command
from mode_enum import Mode

import vk_api
import random
import os.path
from vk_api import keyboard
from vk_api.upload import VkUpload

import urllib
from urllib.request import urlretrieve


class Files:

    @staticmethod
    def files(self, msg) -> list:
        # if msg.startswith(Command.get_audio_file.value[0]):
        #     msg = msg[7::]
        #     return Files.get_audio_file(msg)
        # if msg.startswith(Command.get_video_file.value[0]):
        #     msg = msg[7::]
        #     return Files.get_video_file(msg)
        if msg.startswith(Command.get_searcher_info.value[0]):
            msg = msg[len(Command.get_searcher_info.value[0])+1::]
            return Files.get_searcher_info(self, msg)
        elif msg.startswith(Command.get_document_file.value[0]):
            msg = msg[len(Command.get_document_file.value[0])+1::]
            return Files.get_document_file(self, msg)
        elif msg.startswith(Command.download_files.value[0]):
            msg = msg[len(Command.download_files.value[0])+1::]
            return Files.download_files(self)
        elif msg in Command.main_menu.value:
            return self.change_mode(Mode.default)
        else:
            return "Укажите, что требуется найти"

    # @staticmethod
    # def get_audio_file(msg):
    #     VkUpload.document_message(doc=os.path.abspath(os.curdir), title=msg, tags=None, peer_id=None)

    # @staticmethod
    # def get_video_file(msg):
    #     upload.document_message(doc, title=None, tags=None, peer_id=None)
    #

    # Отправляет документы с заданным названием
    @staticmethod
    def get_document_file(self, msg):

        upload = vk_api.VkUpload(self.vk_session)

        type_files = [".txt", ".pdf", ".jpg", ".py"]
        files_lists = [None for type_file in type_files]
        directory = ".\\sendfiles\\"
        files = os.listdir(directory)

        # Фильтруем список по расширению файлов
        # Поиск всех файлов с расширением type_files[i] и запись их во вложенный список
        for i, type_doc in enumerate(type_files):
            files_lists[i] = filter(lambda x: x.endswith(''.format(type_doc)), files)

        if_files_exist = 0
        # Проход по спискам файлов (по расширению)
        for j, files_list in enumerate(files_lists):
            # Проход по конкретному списку файлов (по расширению)
            for k, file in enumerate(files_list):
                # Если имя файла содержит введённую инфу и оканчивается на нужное расширение
                # Выводим на экран.
                # (Это сделано для того, чтобы файлы не мешались, а выводились группами с одним расширением)
                if file.find(msg) != -1 and file.endswith(type_files[j]):
                    doc_path = directory + file
                    msg_to_send = file[0:file.find(type_files[j])]  # Имя файла без расширения
                    mydoc = upload.document_message(
                        doc_path,
                        # title="docum",
                        # tags=10,
                        peer_id=self.user_id)
                    doc_to_send = mydoc.get('doc')  # Достаем из JSON параметр с документом на сервере
                    attachments = list()

                    # Посылаем документ в ЛС
                    attachments.append('doc{}_{}'.format(doc_to_send['owner_id'], doc_to_send['id']))
                    self.vk_api.messages.send(
                        random_id=random.randint(0, 2048),
                        user_id=self.user_id,
                        message=msg_to_send,
                        attachment=','.join(attachments))

                    if_files_exist += 1
                else:
                    print("Файл с расширением " + type_files[j] + " отсутствует")

        if if_files_exist:
            return "Все файлы предоставлены"
        else:
            return "Таких файлов нет"

    # Постит на стене группы
    @staticmethod
    def wallPost(self):
        vk_session_user = vk_api.VkApi("89535997163", "Element89029912983!")
        vk_session_user.auth()
        vk_api_user = vk_session_user.get_api()

        attachments = Files.save_photoForWall(self, vk_api_user, vk_session_user)

        vk_api_user.wall.post(
            owner_id=self.group_id*-1,
            message='Тестовый пост от бота.',
            attachment= attachments
        )
        return "Пост создан"

    # Выгружает фото на сервер для отправки
    @staticmethod
    def save_photoForWall(self, vk_api_user, vk_session_user):

        # # Путь к картинке
        # file_name = ".\\test.jpg"
        #
        # rs = vk_api_user.photos.getWallUploadServer(group_id=self.group_id)
        # upload_url = rs['upload_url']
        #
        # rs = requests.post(upload_url, files={'photo': open(file_name, 'rb')})
        # rs = json.loads(rs.text)
        # rs = vk_api_user.photos.saveWallPhoto(
        #     server=rs['server'],
        #     photo=rs['photo'],
        #     group_id = self.group_id,
        #     from_group=0,
        #     hash=rs['hash'])
        #
        # # attachments поместить в `vk.method('wall.post'`
        # attachments = 'photo{}_{}'.format(rs[0]['owner_id'], rs[0]['id'])

        # Загрузка картинок на сервера вк и получение их id

        upload = vk_api.VkUpload(vk_session_user)
        photos = ['1.jpg', 'test.jpg']
        photo_list = upload.photo_wall(photos)
        attachments = ','.join('photo{owner_id}_{id}'.format(**item) for item in photo_list)

        return attachments

    # Гуглит в duckduckgo
    @staticmethod
    def get_searcher_info(self, msg):
        session = requests.Session()
        upload = vk_api.VkUpload(self.vk_session)
        resp_for_user = ""
        print('id{}: "{}"'.format(self.user_id, msg), end=' ')

        # Гуглим инфу по запросу
        response = session.get(
            'http://api.duckduckgo.com/',
            params={
                'q': msg,
                'format': 'json'
            }
        ).json()

        # Достаём из json-ответа текст и картинку
        text = response.get('AbstractText')
        image_url = response.get('Image')

        if not text:
            self.vk_api.messages.send(
                user_id=self.user_id,
                random_id=random.randint(0, 2048),
                message='No results'
            )
            print('no results')
            resp_for_user = 'no results'

        attachments = []

        # Пихаем картинку в параметр json для ответа
        if image_url:
            image = session.get(image_url, stream=True)
            photo = upload.photo_messages(photos=image.raw)[0]

            attachments.append(
                'photo{}_{}'.format(photo['owner_id'], photo['id'])
            )

        # Если есть результат, отправляем ответ
        if text:
            self.vk_api.messages.send(
                user_id=self.user_id,
                attachment=','.join(attachments),
                random_id=random.randint(0, 2048),
                message=text
            )
            print('ok')
            resp_for_user = "Информация по запросу предоставлена."

        return resp_for_user

    # Скачивает доки из сообщения
    @staticmethod
    def download_files(self):

        messages = self.vk_api.messages.getConversations(
            offset = 0,
            count = 20,
            filter = 'unanswered')  # Метод, который собирает новые диалоги с неотвеченными сообщениями

        items = messages.get('items')
        last_message = items[0].get('last_message')
        attachments = last_message.get('attachments')
        print(attachments)
        for i, attachment in enumerate(attachments):
            messageDoc = attachment.get('doc')
            print(messageDoc)
            title = messageDoc.get('title')
            url_doc = messageDoc.get('url')
            path = ".\\download_files\\" + title
            urllib.request.urlretrieve(url_doc, path)

        # Пост на стену
        Files.wallPost(self)

        
        return "Файлы загружены"



