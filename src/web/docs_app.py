from flask import Flask, send_from_directory
import os

class SphinxFlaskApp:
    def __init__(self, app_name, sphinx_directory):
        self.app = Flask(app_name)
        self.sphinx_directory = os.path.abspath(sphinx_directory)
        self._setup_routes()

    def _setup_routes(self):
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/<path:filename>', 'documentation', self.documentation)

    def index(self):
        return send_from_directory(self.sphinx_directory, 'index.html')

    def documentation(self, filename):
        return send_from_directory(self.sphinx_directory, filename)

    def run(self, debug=False):
        self.app.run(debug=debug)


sphinx_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../docs/html/'))

if not os.path.exists(sphinx_directory):
    raise FileNotFoundError(f"Directory {sphinx_directory} not found")

if __name__ == '__main__':
    app = SphinxFlaskApp('Sphinx Documentation App', sphinx_directory)
    app.run(True)