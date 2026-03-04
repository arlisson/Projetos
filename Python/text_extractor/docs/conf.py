# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'PreencheFacil'
copyright = '2026, Avance Telecom'
author = 'Avance Telecom'
release = 'v0.0.3'


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",          # entende Google/Numpy style
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
]

html_theme = "sphinx_rtd_theme"
autodoc_member_order = "bysource"
autodoc_mock_imports = ["PyQt5", "PyQt6", "PySide6"]
# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_static_path = ['_static']
