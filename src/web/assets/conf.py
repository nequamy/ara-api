import os
import sys
import time

sys.path.append(os.path.abspath('./docs'))

suppress_warnings = ['image.nonlocal_uri']

project = 'Applied Robotics Avia Wiki'
author = 'Alexander Kleimenov'
copyright = '{}, {}'.format(time.strftime('%Y'), author)
release = 'v0.1'

exclude_patterns = ['**/_*.rst']

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

extensions = [
    'sphinx.ext.graphviz',
    'sphinx.ext.ifconfig',
    'sphinx_copybutton',
    'sphinx_tabs.tabs',
    'sphinx_rtd_theme',
    'sphinxcontrib.mermaid',
    'myst_parser',
]

templates_path = [
    "source/_templates",
]

exclude_patterns = []

language = 'ru'

myst_url_schemes = {
    "https": None,
    "http": None,
    "mailto": None,
}

pygments_style = 'sphinx'

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'analytics_id': 'G-EVD5Z6G6NH',
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': -1,
}

html_static_path = ['_static']
html_use_index = False
html_favicon = 'favicon.ico'
html_baseurl = 'http://docs.ara.org/ru'
