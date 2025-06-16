# GO-IT-ContactProject

Переходимо в діректорію проекту
cd basic_project

Встановлюємо необхідні бібліотеки
pip install django
pip install psycopg2-binary
pip install django-environ

застосовуємо міграцію та сворюємо суперкористувача (адміна)
python3 manage.py migrate
python3 manage.py createsuperuser

Виконуємо перший запуск застосунку на перевірку коректності
python3 manage.py runserver
Шлях до застосутнку - http://127.0.0.1:8000/
Шлях до адмін-панелі - http://127.0.0.1:8000/admin/login/?next=/admin/