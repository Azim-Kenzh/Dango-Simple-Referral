# Применение

## Установка переменных среды

Для корректной работы необходимо настроить в файле следующие переменные среды `.env`:

Введите `Your Value` соответствующие значения, которые вы хотите использовать для каждой переменной.

```commandline
    SECRET_KEY=Your Value
    ALLOWED_HOSTS=localhost
    POSTGRES_DB=Your Value
    POSTGRES_USER=Your Value
    POSTGRES_PASSWORD=Your Value
    POSTGRES_HOST=postgres
    POSTGRES_PORT=Your Value
    CSRF_TRUSTED_ORIGINS=http://localhost
```

## Запуск приложения

#### 1. Сначала вам следует клонировать репозиторий на свой компьютер. Если вы еще этого не сделали, выполните следующую команду:

```
git clone https://github.com/Azim-Kenzh/Dango-Simple-Referral.git
```

#### 2. Перейдите в папку проекта:

```
cd Dango-Simple-Referral
```

#### 3. Запустите Docker Compose:

```
docker-compose up -d --build
```

Это запустит все необходимые службы, перечисленные в вашем файле docker-compose.yml, включая ваше приложение Django, базу данных PostgreSQL и другие.
