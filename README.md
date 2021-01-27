
API Foodgram-project
Сервис для создания вкусных рецептов.

# Getting Started
На сервер переместите в корень  папку nginx, docker-compose.yaml.
Создайте .env с настройками для подключения к БД и с ключом джанго проекта.
- DEBUG=on
- SECRET_KEY=ключ
- DB_ENGINE=django.db.backends.postgresql
- DB_NAME=Имя БД
- POSTGRES_USER=пользователь
- POSTGRES_PASSWORD=пароль
- DB_HOST=db
- DB_PORT=5432


Запуск проекта выполняется командой <docker-compose up --build -d>
 
Далее необходимо выполнить следующий шаги
 - открываем терминал в контейнере web <docker exec -it <container_id> bash>
 - миграция <python manage.py migrate>
 - создаем необходимые таблицы python3 manage.py migrate --run-syncdb
 - заходим в оболочку джанго python3 manage.py shell
 - импортируем ContentType from django.contrib.contenttypes.models import ContentType
 - удаляем ContentType.objects.all().delete()
 - выходим из оболочки quit()
 - загружаем данные в базу данных python3 manage.py loaddata dump.json
 - создаем администратора <python manage.py createsuperuser>
 - заходим по адресу your_domain/admin/ и создаем flatpages

# Built With
Django v3.1.3

# Versioning
На данный момент версия проекта v1. Чтобы узнать доступные версии смотрите теги в этом репозитории.


# Authors
Balashov Konstantin


# Acknowledgments
Спасибо, всем кто воспользовался данным сервисом, буду рад обратной связи.
