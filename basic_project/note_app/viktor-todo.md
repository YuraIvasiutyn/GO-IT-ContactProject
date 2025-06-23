# TODO
+ 1. налаштувати локально енвайрмент
   + 1. створити бранечу
   + 2. створити .env
   + 3. підключити до БД - DBEver
   + 4. продивитися вже існуючий код
   + 5. створити віртуальне оточення      
        ```cmd
        python -m venv %pyenv%\goit_final_project
        %pyenv%\goit_final_project\Scripts\activate.bat
        %pyenv%\goit_final_project\Scripts\deactivatev
        ```
    + 6. встановити і налаштувати poetry
        ```cmd
        pip install poetry
        cd %github%\goit_final_project
        poetry init
        ```
   + 7. встановити потрібні модулі
        ```
        poetry add django
        poetry add psycopg2-binary
        poetry add django-environ
        ```
   + 8. запустити перший раз перевірити основу
        ```cmd
        python manage.py runserver
        ```
2. почати розробку свого модуля
   + 1. передивитися ТЗ
   +2. знайти код лаби - перенести в проект
      + 1. models
      + 2. forms
      + 3. urls
      + 4. views
      + 5. admin
    + 3. templates
        + error.html
        + base.html
        + tag.html
        + note.html
        + note_detail.html
     + notes_by_tag.html
   + 3. вмонтувати в код
   + 4. створити нові таблиці модуля в БД
     ```cmd
     cd %GitHub%\go-it-contactproject\basic_prooject
     python manage.py makemigrations  --name=note_app_1
     python manage.py migrate
     ```
   + 5. зробити сучасну верстку своїх сторінок
      + top_navigation.html
      + base.html
      + error.html
      + index.html
      + tag.html
      + top_10_tags.html
      + note_section.html
      + note.html
      + notes_by_tag.html
     
+ створити requirements.txt
     poetry run pip freeze > requirements.txt
     poetry export -f requirements.txt --output requirements.txt --without-hashes

+ запаблішити десь на хості https://render.com
     + Перейди на https://render.com → New → Web Service
     + Вибери GitHub репозиторій
     + Python environment
     + Назви start command:
          gunicorn basic_project.wsgi:application
     + Увімкни авто-deploy
     + Додай DJANGO_SECRET_KEY, DEBUG=False, ALLOWED_HOSTS
-----
2025-06-20
+ як закріпити верхнє меню щоб воно завжди було видиме, навіть при прокрутці?
+ додати меню для інших модулів сайту
+ додати підменю для нотаток
+ додати сортування нотаток по зростанню/спаданню
+ зняти код з дев гілки + conflict resolve
+ запаблішити нову версію коду на render
+ вмерджити свої зміни в дев-гілку
----
2025-06-21
     + пофіксити проблему з "пошуком"
     + пофіксити проблему що карточки перетасовуються після змін - додати сорутвання по Ід за замовчуванням
     + додати можливість змінювати кольори нотаток  
          + python manage.py makemigrations --name=note_app_add_colornote
          + python manage.py migrate
          + підібрати 10 кольорів які добре виглядають на світлій і темній схемі
          + 1 кнопка випьбрати власнийц колі
     + вмонтувати нашу кастомну error-page
     + додати редагування і видалення тегів
     ------
     + запаблішити
          + закомітити свою гілку
          + витягнути дев гілку
          + підправити лінки з головної сторінки і меню
          + перепаблішити аплікейшин сайт
          + вмерджити свої зміни в дев гілку
     
2025-06-22
     причесати код
     задокументувати

# Bugs
     * коли на нотатках нажимаєш "Last" виводяться всі нотатки
     * проблема із вспливаючим меню, воно перекоривається наступними карточками

Як покращити UI:
     Зроби кожну кнопку кольору з тонкою рамкою при виборі.
     Додай активну підсвітку до вибраного кольору (наприклад, box-shadow або border: 2px solid).
-----------------
# Test
+ видалення неіснуюючої нотатки
     http://localhost:8000/note/note/delete/100/
+ спроба редагувати неіснуючу нотатку
     http://localhost:8000/note/note/edit/100
     http://localhost:8000/note/note/edit/sdfsdfdsf
+ спроба проапдейтити колір в неіснуючій нотатці
     http://localhost:8000/note/note/color/100
+ пошук по неіснуючому тегу
     http://localhost:8000/note/tag/111
видалення нотатки що належить іншому користувачу
-----------------
# Final actions для production-режиму
1. Django settings file
     DEBUG = False
     ALLOWED_HOSTS = ['your-app-name.onrender.com']
2. кастомна обробка помилок
     У головному urls.py:
          handler404 = 'note_app.views.custom_404'
          handler500 = 'note_app.views.custom_500'
     
     А у views.py :
          def custom_404(request, exception):
          return redirect_to_error("⛔ Page not found (404)")

          def custom_500(request):
          return redirect_to_error("💥 Server error (500)")