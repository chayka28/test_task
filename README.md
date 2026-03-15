# Trendsee Test Project

Репозиторий подготовлен под тестовое задание с разделением на независимые папки:

- `backend/` — FastAPI + PostgreSQL + Redis
- `frontend/` — отдельная зона под фронтенд-часть (по Figma, можно развивать дальше)

## Структура проекта

```text
TT/
  backend/
    app/
      api/
      core/
      db/
      dependencies/
      repositories/
      schemas/
      services/
      main.py
    Dockerfile
    requirements.txt
    .env.example
  frontend/
    README.md
  docker-compose.yml
  postman_collection.json
```

## Backend архитектура (слои)

1. `api` — роуты и HTTP-слой.
2. `services` — бизнес-логика.
3. `repositories` — SQL-запросы в PostgreSQL (параметризованные).
4. `dependencies` — Dependency Injection для сервисов, репозиториев и авторизации.
5. `db` — подключение к PostgreSQL/Redis и SQL-инициализация таблиц.

## Что реализовано по ТЗ

### Пользователи

- Создать пользователя (возвращается JWT)
- Получить JWT по `user_id`
- Изменить имя пользователя
- Удалить пользователя

### Публикации

- Создать публикацию (только с JWT)
- Изменить публикацию (только автор)
- Удалить публикацию (только автор)
- Получить все публикации пользователя

### Кэширование

- Чтение публикаций пользователя: сначала Redis.
- Если кэша нет: чтение из PostgreSQL + искусственная задержка `2s` (`asyncio.sleep(2)`).
- TTL кэша публикаций: `10 минут` (`600` секунд).

## Запуск

```bash
docker-compose up --build
```

После запуска:

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- OpenAPI: `http://localhost:8000/openapi.json`

## Эндпоинты

Префикс API: `/api/v1`

### Users

- `POST /api/v1/users` — создать пользователя + токен
- `GET /api/v1/users/{user_id}/token` — получить токен по id
- `PATCH /api/v1/users/{user_id}` — изменить имя
- `DELETE /api/v1/users/{user_id}` — удалить пользователя

### Posts

- `POST /api/v1/posts` — создать публикацию (Bearer token)
- `PATCH /api/v1/posts/{post_id}` — изменить публикацию (Bearer token, только автор)
- `DELETE /api/v1/posts/{post_id}` — удалить публикацию (Bearer token, только автор)
- `GET /api/v1/posts/user/{user_id}` — получить публикации пользователя

## Postman

Коллекция находится в файле:

- `postman_collection.json`

В коллекции есть переменные `base_url`, `token`, `user_id`, `post_id`.
