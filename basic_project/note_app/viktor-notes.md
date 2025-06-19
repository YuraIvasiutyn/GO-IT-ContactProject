# DB
* 256 MB RAM
* 0.1 CPU
* 1 GB Storage

Permissions:
* hostname: dpg-d18094emcj7s73cd9300-a.frankfurt-postgres.render.com
* port: 5432
* Database: contacts_base
* username: admin
* password: fk3YJeFa2r7eTfxKVRgRfuxIfUikFSaK
-----
# settings
вміст .env (потрібно створити всередині basic_project)
```
SECRET_KEY=django-insecure-=dws00y1frho2hk$s6#pt4v5pz(yif6g4fi_h*bm5#sar#1rvk
DATABASE_NAME=contacts_base
DATABASE_USER=admin
DATABASE_PASSWORD=fk3YJeFa2r7eTfxKVRgRfuxIfUikFSaK
DATABASE_HOST=dpg-d18094emcj7s73cd9300-a.frankfurt-postgres.render.com
DATABASE_PORT=5432
```
-----
# Домоволеності
* Перед роботою з гітхабом створіть кожен свою гілку на гітхаб (перед цим мені потрібні нікнейми щоб вас додати до проекту на гітхаб)
* файл .env потрібно створити всередині basic_project
* стендап 19:00
-----
* накатуємо міграційні скріпти в БД
```cmd
cd %GitHub%\goit-web-hw-13\part_1
alembic upgrade head
```
1. виконати міграцію джанго-моделі в БД
```cmd
cd %GitHub%\go-it-contactproject\basic_prooject
python manage.py migrate
```

2. створення супер-юзера
```cmd
python manage.py createsuperuser
```

3. **run server**
```cmd
cd %GitHub%\goit-web-hw-13\part_2
python manage.py runserver
```
-----------------------------------------------------------------
# Documentation
1. poetry add sphinx -G dev
2.  в корені проекту виконати
    sphinx-quickstart docs
3.  запускаємо
    .\make.bat html
4.  make clean
make html
------
# usefull references
* Шлях до застосутнку - http://127.0.0.1:8000/
* Шлях до адмін-панелі - http://127.0.0.1:8000/admin/login/?next=/admin/

http://127.0.0.1:8000/dev-login
http://127.0.0.1:8000/notes-main
http://127.0.0.1:8000/tag
http://127.0.0.1:8000/tag/1
http://127.0.0.1:8000/note/
http://127.0.0.1:8000/note/1
http://127.0.0.1:8000/note/edit/1
http://127.0.0.1:8000/note/delete/1

Django super user
user: viktor
pass: 123456
------
# questiuos to discuss with team
1. need to poetry or requirements file with allo isntalled modules?
2. python version - 3.11.4?
3. home page - з якої всі стартують? чи може зробемо в базовому теплейті менюшку?
4. Вітаю, сьогодні приступив до реалізації, в нас вже є якийсь базовий django-шаблон?
5. також потрібна спільна error-page
6. в ТЗ сказано "Здійснювати сортування нотаток за ключовими словами (тегами)" а як сортувати якщо нотатка має декілька тегів?
---------------------------
1. чи будемо робити sphinx - документацію?
2.  покриття свого коду тестами?
3.  addded postman file with API requests


