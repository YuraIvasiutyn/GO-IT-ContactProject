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
pip install whitenoise
pip install pyuploadcare

```
3. застосовуємо міграцію та сворюємо суперкористувача (адміна)
```cmd
python manage.py migrate
python manage.py createsuperuser
```
4. потрібно створити `.env` файл в середині `basic_project` папці
```
SECRET_KEY=secret
DATABASE_NAME=db-name
DATABASE_USER=db-user
DATABASE_PASSWORD=password
DATABASE_HOST=host
DATABASE_PORT=5432
PUBLIC_KEY=secret
EMAIL_HOST=smtp.meta.ua
EMAIL_PORT=465
EMAIL_HOST_USER=xxx@meta.ua
EMAIL_HOST_PASSWORD=email-password
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
DEFAULT_FROM_EMAIL=Personal Assistant <xxx@meta.ua>
USE_CREDENTIALS=True
VALIDATE_CERTS=True
```

5. Виконуємо перший запуск застосунку на перевірку коректності
```cmd
python manage.py runserver
```

## Usefull Commands
* як створити документацію?
```cmd
cd docs
make html
```

## Links
* Шлях до застосутнку - http://127.0.0.1:8000/
* Шлях до адмін-панелі - http://127.0.0.1:8000/admin/login
* Шлях до документації - 