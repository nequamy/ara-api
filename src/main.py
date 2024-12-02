import multiprocessing
import os
import sys
import time
import logging
from contextlib import redirect_stdout, redirect_stderr

from gui.app_gui import GUI
from navigation.nav_service import NavigationManagerGRPC, serve as nav_serve
from web.docs_app import SphinxFlaskApp
from web.app import run
from driver.msp_service import main as msp_main

class ServiceManager:
    """
    Manages the lifecycle of multiple services running in parallel.
    """

    def __init__(self):
        """
        Initializes the ServiceManager with necessary configurations.
        """
        self.gui = GUI()
        self.gui.run()

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

    def run_dash_app(self):
        """
        Runs the Dash application.
        """
        self.logger.info("Starting Dash app")
        try:
            with open(os.devnull, 'w', encoding='utf-8') as f, \
                 redirect_stdout(f), redirect_stderr(f):
                run()
        except Exception as e:
            self.logger.error("Error starting Dash app: %s", e)

    def run_sphinx_app(self):
        """
        Runs the Sphinx application.
        """
        try:
            self.logger.info("Starting Sphinx app")
            with open(os.devnull, 'w', encoding='utf-8') as f:
                sys.stdout = f
                sys.stderr = f
                sphinx_flask_app = SphinxFlaskApp('ara api documentation', self.sphinx_directory)
                sphinx_flask_app.run()
        except Exception as e:
            self.logger.error("Error starting Sphinx app: %s", e)

    def run_nav_service(self):
        """
        Runs the Navigation service.
        """
        try:
            self.logger.info("Starting Navigation service")
            nav_serve()
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
            multiprocessing.Process(target=self.run_dash_app, name="DASH"),
            multiprocessing.Process(target=self.run_sphinx_app, name="SPHINX"),
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

if __name__ == '__main__':
    manager = ServiceManager()
    manager.start_services()
    manager.monitor_services()