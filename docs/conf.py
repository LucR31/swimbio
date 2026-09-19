# Configuration file for the SWIM documentation.
#
# This file is executed by Sphinx when the documentation is built.

import os
import sys

# -- Path setup --------------------------------------------------------------

# If you later want Sphinx to automatically document the Python package,
# add its path here.
#
# Example:
# sys.path.insert(0, os.path.abspath("../python"))

# -- Project information -----------------------------------------------------

project = "SWIM"
copyright = "2026, Luc R."
author = "Luc R."

release = "1.0"
version = "1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
]

templates_path = ["_templates"]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
]

source_suffix = {
    ".rst": "restructuredtext",
}


intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

html_theme = "sphinx_rtd_theme"

html_title = "SWIM Documentation"

html_logo = None

html_static_path = ["_static"]

html_theme_options = {
    "navigation_depth": 4,
    "collapse_navigation": False,
    "sticky_navigation": True,
    "includehidden": True,
    "titles_only": False,
}

html_context = {
    "display_github": True,
    "github_user": "LucR31",
    "github_repo": "swimbio",
    "github_version": "main",
    "conf_py_path": "/docs/",
}

nitpicky = False