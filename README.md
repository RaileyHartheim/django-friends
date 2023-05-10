## Django Friends
Django Friends - сервис, предоставляющий следующие возможности:
- зарегистрироваться как новый пользователь;
- отправить заявку в друзья другому пользователю;
- принять или отклонить заявку в друзья от другого пользователя;
- просматривать списки входящих и исходящих заявок в друзья;
- просматривать список своих друзей;
- узнавать свой статус дружбы с другим пользователем на странице этого пользователя;
- при необходимости удалить другого пользователя из друзей.


Если пользователь отправил вам заявку в друзья, а вы отправляете заявку ему - вы автоматически становитесь друзьями.


Бэкенд реализован на Django 3.2.18 и Django REST Framework 3.12.4.

### Установка проекта
Все нижеперечисленные команды указаны для терминала bash

- Клонируйте репозиторий:

```
git clone git@github.com:RaileyHartheim/django-friends.git
cd django-friends/
```

- Cоздайте виртуальное окружение и активируйте его:

```
python3 -m venv .venv
source .venv/bin/activate
```

- Установите зависимости из requirements.txt:

```
pip install -r requirements.txt
```

- Сгенерируйте через django-admin shell секретный ключ:
```
django-admin shell
>>>from django.core.management.utils import get_random_secret_key  
>>>get_random_secret_key()
<сгенерированный ключ>
```

- Создайте файл .env в папке с settings.py и заполните его полученным ключом:
```
SECRET_KEY = <сгенерированный ключ>
```

- Выполните миграции:

```
cd django-friends/
python manage.py migrate
```

- При необходимости создайте суперпользователя:

```
python manage.py createsuperuser
```

- Запустите проект:

```
python manage.py runserver
```

Созданным суперпользователем при желании можно войти в админку для просмотра пользователей и заявок в друзья по адресу:

```
http://127.0.0.1:8000/admin/
```

### Документация к API

- через Swagger:
```
http://127.0.0.1:8000/api/swagger/
```

- через Redoc:
```
http://127.0.0.1:8000/api/redoc/
```

### Эндпоинты и примеры запросов



- POST: ```http://127.0.0.1:8000/api/users/``` - создание нового пользователя
```
Запрос: 
{
    "username": "username",
    "password": "password"
}
```
- POST: ```http://127.0.0.1:8000/api/auth/jwt/create/``` - получение JWT-токена

Запрос: 
```
{
    "username": "username",
    "password": "password"
}
```

Ответ:
```
{"refresh": <сгенерированный токен>,
"access": <сгенерированный токен>}
```

После этого для авторизации нужно передавать в заголовках пару ключ-значение ```Authorization: Bearer <"access"-токен>```

- GET: ```http://127.0.0.1:8000/api/users/me/``` - просмотр своего профиля

Пример ответа:
```
{
    "id": 4,
    "username": "dean",
    "is_in_friendship": "Это ваш профиль"
}
```

- GET: ```http://127.0.0.1:8000/api/users/<user_id>/``` - просмотр любого пользователя

Пример ответа:
```
{
    "id": 2,
    "username": "bert",
    "is_in_friendship": "Вы не друзья"
}
```

- POST: ```http://127.0.0.1:8000/api/users/<user_id>/add_friend/``` - отправление заявки в друзья

Пример ответа:
```
{"sender":4,"receiver":2}
```

- GET: ```http://127.0.0.1:8000/api/users/``` - просмотр всех пользователей

Пример ответа:
```
[{"id":1,"username":"alice","is_in_friendship":"Вы не друзья"},{"id":2,"username":"bert","is_in_friendship":"Вы направили этому пользователю заявку в друзья"},{"id":3,"username":"chloe","is_in_friendship":"Этот пользователь направил вам заявку в друзья"},{"id":4,"username":"dean","is_in_friendship":"Это ваш профиль"}]
```

- GET: ```http://127.0.0.1:8000/api/requests/incoming/``` - просмотр входящих заявок

Пример ответа:
```
[{"id":4,"sender":3}]
```

- POST: ```http://127.0.0.1:8000/api/requests/incoming/<request_id>/accept_request/``` - принять входящую заявку в друзья

Пример ответа:
```
{"id":3,"username":"chloe","is_in_friendship":"Вы друзья"}
```

- GET: ```http://127.0.0.1:8000/api/users/friends/``` - получить список друзей

Пример ответа:
```
[{"id":3,"username":"chloe","is_in_friendship":"Вы друзья"}]
```

- DELETE: ```http://127.0.0.1:8000/api/users/friends/<user_id>/delete_friend/``` - удалить человека из друзей

После этого запрос по ссылке GET: ```http://127.0.0.1:8000/api/users/friends/``` может выглядеть вот так:
```
[]
```

- GET: ```http://127.0.0.1:8000/api/requests/outcoming/``` - просмотр исходящих заявок
Пример ответа:
```
[{"id":5,"receiver":2}]
```

