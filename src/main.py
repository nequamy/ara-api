import multiprocessing
import os
import sys
import time
import logging
import asyncio
from contextlib import redirect_stdout, redirect_stderr
import platform

import colorama
import pyfiglet
from colorama import Fore

from navigation.nav_service import NavigationManagerGRPC, serve as nav_serve
from driver.msp_service import main as msp_main


system = platform.system()
if system == "Windows":
    multiprocessing.set_start_method('spawn')
elif system in ["Linux", "Darwin"]:  # Darwin is macOS
    multiprocessing.set_start_method('fork')


class ServiceManager:
    """
    Manages the lifecycle of multiple services running in parallel.
    """

    def __init__(self):
        """
        Initializes the ServiceManager with necessary configurations.
        """
        self.ascii_art = pyfiglet.figlet_format("ARA MINI API v0.8.0", font="slant", width=50)
        self.summary = ("Поздравляем! Вы запустили API для программирования ARA MINI\n\n"
                        "Документация запущена на адресе: http://127.0.0.1:5000/\n"
                        # "WEB-приложение запущено на адресе: http://127.0.0.1:8050/\n\n"
                        "Для подключения в конфигуратеоре:\n"
                        "\tUDP: \thttp://192.168.2.113:14550\n"
                        "\tTCP: \thttp://192.168.2.113:5760\n\n"
                        "Изображение с камеры: \t\thttp://192.168.2.113:81/stream\n")

        self.gui_run()

        self.sphinx_directory = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '../docs/html/')
        )
        self.processes = []
        self.__init_logging__('log')

    def __init_logging__(self, log_directory='log'):
        """
        Sets up logging configuration for the service manager.
        """
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        self.logger = logging.getLogger('service_manager')
        self.logger.setLevel(logging.INFO)
        self.logger_formater = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger_handler = logging.FileHandler(os.path.join(log_directory, 'service_manager.log'))
        self.logger_handler.setFormatter(self.logger_formater)
        self.logger.addHandler(self.logger_handler)
    
    def gui_run(self):
        colorama.init()

        print(Fore.BLUE + self.ascii_art)
        print("=" * 60)
        print("\n")
        print(Fore.CYAN + self.summary)

        # print(Fore.RED + "Data output:")
        print(Fore.MAGENTA)
        colorama.deinit()

    def run_nav_service(self):
        """
        Runs the Navigation service.
        """
        try:
            self.logger.info("Starting Navigation service")
            asyncio.run(nav_serve())
        except Exception as e:
            self.logger.error("Error starting Navigation service: %s", e)

    def run_msp_service(self):
        """
        Runs the MSP service.
        """
        try:
            self.logger.info("Starting MSP service")
            msp_main()
        except Exception as e:
            self.logger.error("Error starting MSP service: %s", e)

    def start_services(self):
        """
        Starts all the services as separate processes.
        """
        self.processes = [
            multiprocessing.Process(target=self.run_nav_service, name="NAV"),
            multiprocessing.Process(target=self.run_msp_service, name="MSP")
        ]

        for process in self.processes:
            try:
                self.logger.info("Starting process %s", process.name)
                process.start()
            except Exception as e:
                self.logger.error("Error starting process %s: %s", process.name, e)

    def monitor_services(self):
        """
        Monitors the services and logs their status.
        """
        try:
            while True:
                for process in self.processes:
                    if not process.is_alive():
                        self.logger.warning("%s process has terminated.", process.name)
                        return
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Terminating processes due to KeyboardInterrupt")
            self.terminate_services()
        except Exception as e:
            self.logger.error("Error monitoring services: %s", e)
            self.terminate_services()

    def terminate_services(self):
        """
        Terminates all running services.
        """
        for process in self.processes:
            try:
                self.logger.info("Terminating process %s", process.name)
                process.terminate()
                process.join()
            except Exception as e:
                self.logger.error("Error terminating process %s: %s", process.name, e)
        self.logger.info("All processes terminated.")


def main():
    manager = ServiceManager()
    manager.start_services()
    manager.monitor_services()

if __name__ == "__main__":
    main()