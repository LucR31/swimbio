project = "SWIM"
copyright = "2026, Luc R."
author = "Luc R."

version = "1.0"
release = "1.0"

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
]

templates_path = []

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

html_theme_options = {
    "navigation_depth": 4,
    "collapse_navigation": False,
    "sticky_navigation": True,
    "includehidden": True,
    "titles_only": False,
}

nitpicky = False