Notes module 
============

Overview
---------
This section documents all parts of the **Notes** module in the Personal Assistant application.

.. contents::
   :depth: 2
   :local:

Urls
-----
Routes that define how the application maps URL paths to views.

.. automodule:: note_app.urls
   :members:
   :undoc-members:
   :show-inheritance:
   :noindex:

Views
------
Business logic and presentation rendering for notes and tags.

.. currentmodule:: note_app.views

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   redirect_to_error
   count_top_tags
   get_notes_on_page
   main
   tag
   edit_tag
   note
   note_detail
   note_delete
   search_by_tag
   update_note_color
   delete_tag

Forms
-----
Form definitions for user input handling.

.. automodule:: note_app.forms
    :no-members:
    :no-inherited-members:
    :noindex:

TagForm
^^^^^^^^
.. autoclass:: note_app.forms.TagForm
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

NoteForm
^^^^^^^^^
.. autoclass:: note_app.forms.NoteForm
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:


Data models
------------
Models defining the structure of notes and tags.

.. automodule:: note_app.models
   :no-members:
   :no-inherited-members:
   :noindex:

Tag
^^^
.. autoclass:: note_app.models.Tag
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: DoesNotExist, MultipleObjectsReturned
   :no-index:

Note
^^^^
.. autoclass:: note_app.models.Note
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: DoesNotExist, MultipleObjectsReturned
   :no-index:
