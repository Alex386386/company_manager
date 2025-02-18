# Система управления юзерами, компаниями и прилегающими моделями

## Содержание

1. [Стек технологий](#стек-технологий)
2. [Назначение проекта](#назначение-проекта)
3. [Основная информация по использованию API](#основная-информация-по-использованию-api)
4. [Установка и запуск](#установка-и-запуск)
5. [Тесты](#тесты)
6. [Автор](#автор)

## Стек технологий

- **Python**: 3.12.9
- **FastAPI**: 0.115.8
- **База данных**: PostgreSQL 17

## Назначение проекта

Система разработана по схеме БД и минимальному тех.заданию предоставленному для выполнения тестового задания.
По сути представляющею собой контейнеры для CRUD операций с основными моделями.
6 контейнеров:

- БД;
- Сервис авторизации;
- Сервис регистрация пользователей и компаний;
- Сервис создания групп и ролевых моделей;
- Сервис распределения функций пользователей по ролям;
- Сервис создания и редактирование настроек.

Каждый сервис расположен внутри отдельного контейнера, подключаться для просмотра схемы api и работы можно по следующим
адресам:

1. service_auth - http://localhost:8000/docs
2. companies_users_servise - http://localhost:8001/docs
3. functions_servise - http://localhost:8002/docs
4. groups_roles_servise - http://localhost:8003/docs
5. settings_servise - http://localhost:8004/docs

Все контейнеры делят общую директорию управления сущностями БД(**common_models**), так как в проекте использована только
одна БД.

## Основная информация по использованию API

В проекте по запуску создаётся тестовый пользователь и модели необходимые для его создания.

Для обращения к API всех сервисов необходимо получить токен из сервиса service_auth, для его получения вам понадобятся
следующие данные:
**username="string" password="string"**

Так же в проекте можно обновить токен через refresh-эндпоинт, так как по умолчанию промежуток жизни основного токена 15
минут, или получить новый.

## Установка и запуск

Клонировать репозиторий и перейти в него:

```
git clone https://github.com/Alex386386/company_manager.git
cd company_manager/
```

Создайте файл **.env** в корне проекта со следующим содержанием:

```
# Данные PostgreSQL
DB_ENGINE=postgresql+asyncpg
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=qwertyytrewq
DB_HOST=db
DB_PORT=5432
DATABASE_URL="postgresql+asyncpg://postgres:qwertyytrewq@db:5432/postgres"

# Данные формирования токенов
SECRET_KEY="secret-variable"
REFRESH_SECRET_KEY="refresh-secret-variable"
ALGORITHM="HS256"
TOKEN_EXPIRED_MINUTES=15
REFRESH_TOKEN_EXPIRE_MINUTES=600
```

Данные можно оставить без изменений или заменить на свои.

Запустить проект:

```
sudo docker compose --env-file .env up --build
```

Для наглядности работы системы уровень логирования установлен на DEBUG.
Так же для упрощения все логи записываются в поток исполнения.

## Тесты

Для запуска тестов нужно создать файл окружения для тестов **.test.env** со следующим содержанием:

```
# Данные PostgreSQL
DB_ENGINE=postgresql+asyncpg
DB_NAME=test_db
POSTGRES_USER=test_user
POSTGRES_PASSWORD=test_pass
DB_HOST=localhost
DB_PORT=5432
TEST_DATABASE_URL="postgresql+asyncpg://test_user:test_pass@localhost:5433/test_db"

# Данные формирования токенов
SECRET_KEY="secret-variable"
REFRESH_SECRET_KEY="refresh-secret-variable"
ALGORITHM="HS256"
TOKEN_EXPIRED_MINUTES=15
REFRESH_TOKEN_EXPIRE_MINUTES=600
```

Установить зависимости из файла requirements.txt в корне проекта:

```
pip install -r requirements.txt
```

После установки зависимостей запустить тестовую БД командой:

```
sudo docker compose -f test-docker-compose.yaml up -d
```

После, запустить тесты:

```
pytest
```

Следующей командой можно удалить контейнер тестовой БД и её том:

```
sudo docker compose -f test-docker-compose.yaml down -v
```

## Автор

- [Александр Мамонов](https://github.com/Alex386386) 
