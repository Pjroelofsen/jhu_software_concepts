# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os, sys
# instead of '../../src' use '..\..' to land at your project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',    # if you use Google- or NumPy-style docstrings
    'sphinx.ext.viewcode',
]
html_theme = 'sphinx_rtd_theme'  # nice sidebar + search out of the box

project = 'pizza_app'
copyright = '2025, Phil Roelofsen'
author = 'Phil Roelofsen'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ['_static']
