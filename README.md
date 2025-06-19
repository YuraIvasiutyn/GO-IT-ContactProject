# GO-IT-ContactProject
1. Переходимо в діректорію проекту
```cmd
cd basic_project
```
2. Встановлюємо необхідні бібліотеки
```
pip install django
pip install psycopg2-binary
pip install django-environ
```
3. застосовуємо міграцію та сворюємо суперкористувача (адміна)
```cmd
python manage.py migrate
python manage.py createsuperuser
```
4. Виконуємо перший запуск застосунку на перевірку коректності
```cmd
python3 manage.py runserver
```
* Шлях до застосутнку - http://127.0.0.1:8000/
* Шлях до адмін-панелі - http://127.0.0.1:8000/admin/login/?next=/admin/