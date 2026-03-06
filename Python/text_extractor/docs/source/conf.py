import os
import sys
sys.path.insert(0, os.path.abspath("../.."))

project = "PreencheFacil"
author = "Avance Telecom"
release = "v0.0.3"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
]

autodoc_member_order = "bysource"
autodoc_mock_imports = ["PyQt5", "PyQt6", "PySide6"]

html_theme = "furo"