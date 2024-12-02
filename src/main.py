import multiprocessing
import os
import sys
import time
from gui.app_gui import GUI
from navigation.nav_service import NavigationManagerGRPC
from web.docs_app import SphinxFlaskApp
from web.app import run
from driver.msp_service import main as msp_main

sphinx_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../docs/html/'))

def run_dash_app():
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')
    run()

def run_sphinx_app():
    print("Sphinx is running on http://127.0.0.1:5000/\n")
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')
    sphinxFlaskApp = SphinxFlaskApp('ara api documentation', sphinx_directory)
    sphinxFlaskApp.run()

if __name__ == '__main__':
    dash_process = multiprocessing.Process(target=run_dash_app, name="DASH")
    sphinx_process = multiprocessing.Process(target=run_sphinx_app, name="SPHINX")

    dash_process.start()
    sphinx_process.start()

    try:
        while True:
            if not dash_process.is_alive():
                print("Dash process has terminated.")
                break
            if not sphinx_process.is_alive():
                print("Sphinx process has terminated.")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("Terminating processes...")
        dash_process.terminate()
        sphinx_process.terminate()

    dash_process.join()
    sphinx_process.join()

    print("Both processes terminated.")