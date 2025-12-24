# FastAPI шаблон

Шаблон асинхронного FastAPI-приложения с SQLAlchemy, Alembic и готовым docker-compose для PostgreSQL.

## Стек и требования
- FastAPI, SQLAlchemy (async), Alembic.
- Docker + Docker Compose.
- Python ≥3.12 (в `pyproject.toml` указан ^3.14; используйте последнюю стабильную).
- Poetry.
- `app/.env` используется и приложением, и `docker-compose` для поднятия Postgres (переменные `POSTGRES_*`).

## Быстрый старт
1. Клонируйте репозиторий и перейдите в него: `cd /Users/andrejganza/python/pytask`.
2. Скопируйте пример окружения: `cp app/.env.template app/.env`.
3. Обновите креды в `app/.env` (они же попадут в Postgres-контейнер) и приведите `APP_CONFIG__DB__URL` в соответствие, например:\
   `POSTGRES_DB=app`, `POSTGRES_USER=app`, `POSTGRES_PASSWORD=app`, `APP_CONFIG__DB__URL=postgresql+asyncpg://app:app@localhost:5432/app`. `APP_CONFIG__DB__ECHO=1` включает лог SQL.
4. Поднимите базу: `docker compose up -d`.
5. Установите зависимости: `poetry install`.
6. Примените миграции: `poetry run alembic -c app/alembic.ini upgrade head`.
7. Запустите API:\
   `poetry run uvicorn app.main:main_app --reload --host 0.0.0.0 --port 8000`.
8. Откройте Swagger: http://127.0.0.1:8000/docs (эндпоинты под `/api`, а при использовании v1 — под `/api/v1/...`).

## Работа с миграциями
- Создать ревизию из моделей:\
  `poetry run alembic -c app/alembic.ini revision --autogenerate -m "описание"`.
- Применить: `poetry run alembic -c app/alembic.ini upgrade head`.
- Откатить: `poetry run alembic -c app/alembic.ini downgrade -1`.
- Как добавить новую миграцию (рекомендуемый порядок):
  1) Запустите Postgres (`docker compose up -d`) и убедитесь, что `APP_CONFIG__DB__URL` в `app/.env` указывает на рабочую БД.
  2) Обновите модели SQLAlchemy (наследники `core.models.base.Base`).
  3) Сгенерируйте ревизию: `poetry run alembic revision --autogenerate -m "описание"`.
  4) Проверьте сгенерированный файл в `app/alembic/versions/`: операторы `op.add_column`, `op.create_table` и т.п. должны соответствовать ожидаемым изменениям. Если Alembic не увидел разницу, проверьте импорты моделей в `core/models/__init__.py` и маппинги.
  5) Примените миграцию: `poetry run alembic -c app/alembic.ini upgrade head`. При ошибке корректируйте файл ревизии вручную (функции `upgrade`/`downgrade`) и повторите.

## Структура и расширение
- Модели: наследуйте от `core.models.base.Base`; имя таблицы строится из имени класса (CamelCase → snake_case + `s`) через `utils/case_converter.py`.
- Сессии БД: используйте зависимость `db_helper.session_getter`.
- Роуты: добавляйте модули в `app/api` (например, `api/api_v1/...`) и подключайте через `api/router` в `app/main.py`. Общий префикс задаётся `APP_CONFIG__API__PREFIX` (по умолчанию `/api`), версия — `APP_CONFIG__API__V1__PREFIX` (по умолчанию `/v1`).
- Настройки: задаются переменными с префиксом `APP_CONFIG__...` (см. `core/config.py`). Host/port сервера можно переопределить `APP_CONFIG__RUN__HOST` и `APP_CONFIG__RUN__PORT`.
- Переменные `POSTGRES_*` лежат в `app/.env` и используются только docker-compose; приложение их игнорирует.

## Утилиты
- Форматирование: `poetry run black app`.
- Полный сброс БД-контейнера: `docker compose down -v` (удалит данные).

## TODO

Добавить CI/CD для форматирования black
