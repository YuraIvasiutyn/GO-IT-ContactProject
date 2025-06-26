import os
import sys
import django
# Додаємо один рівень вище до PYTHONPATH (відносно розташування conf.py)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Вказуємо Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'basic_project.settings'

# Ініціалізуємо Django
django.setup()

# -- Project information -----------------------------------------------------
project = 'Personal_Assistant'
copyright = '2025, Go IT group #6'
author = 'Go IT - group #6'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',      # якщо docstrings у стилі Google або NumPy
    # 'sphinx.ext.viewcode',      # опціонально, щоб бачити вихідний код у документації
    'sphinx.ext.autosummary',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'nature'
html_theme = 'classic'
html_static_path = ['_static']

# -- Autodoc configuration ---------------------------------------------------
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
    # 'private-members': False,
    # 'special-members': '__init__',
    # 'inherited-members': True,
}

# Якщо хочеш, щоб всі docstrings оброблялися як rst (приклад: __init__)
# autoclass_content = "both"

# Рекомендується додати:
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_private_with_doc = False

# Щоб кожна функція мала заголовок
autodoc_docstring_signature = True
autosummary_generate = True