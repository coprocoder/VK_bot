
# Импортируем созданный нами класс Server
from server import Server
# Получаем из config.py наш api-token
from config import vk_api_token


server1 = Server(vk_api_token, 191612819 , "server1")
print("Бот запущен")
server1.start()
