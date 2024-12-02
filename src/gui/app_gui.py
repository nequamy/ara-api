import colorama
import pyfiglet
from colorama import Fore

# TODO: в версии v0.2 графический интейрфейс пользователя будет доступен только в виде обычного терминального окошка с выводом информации согласно конфигурационному файлу

class GUI():
    def __init__(self):
        self.ascii_art = pyfiglet.figlet_format("ARA MINI API v0.2", font="slant", width=50)
        self.summary = ("Поздравляем! Вы запустили API для программирования ARA MINI\n\n"
                        "Документация запущена на адресе: http://127.0.0.1:5000/\n"
                        "WEB-приложение запущено на адресе: http://127.0.0.1:8050/\n\n"
                        "Для подключения в конфигуратеоре:\n"
                        "\tUDP: \thttp://192.168.2.1:14550\n"
                        "\tTCP: \thttp://192.168.2.1:5760\n\n"
                        "Изображение с камеры: \t\thttp://192.168.2.113:81/stream\n")

    # TODO: реализовать вывод данных в интерфейс пользователя
    def show_data(self):
        pass

    # TODO: обновление новых данных согласно конфигу
    def update_data(self):
        pass

    # TODO: описать чтение конфиг файла для понимания какие данные и в каком формате следует отображать
    def read_config(self):
        pass

    # TODO: реализовать запуск приложения
    def run(self):
        colorama.init()

        print(Fore.BLUE + self.ascii_art)
        print("=" * 60)
        print(Fore.CYAN + self.summary)

        print(Fore.RED + "Data output:")
        print(Fore.MAGENTA)
        colorama.deinit()