# Trendsee

Trendsee — fullstack-приложение для работы с лентой публикаций.

Backend реализован на FastAPI и PostgreSQL, для кэширования используется Redis, авторизация выполнена через JWT. Frontend реализован на Vue 3 и подключен к backend API. При старте проекта автоматически создается витринная лента с демонстрационными авторами и публикациями, чтобы приложение можно было сразу показать в рабочем состоянии.

## Краткое описание структуры проекта

```text
.
├── backend/
│   ├── app/
│   │   ├── api/             # HTTP-роуты
│   │   ├── core/            # конфигурация и безопасность
│   │   ├── db/              # подключение к Postgres и Redis, init.sql
│   │   ├── dependencies/    # Dependency Injection провайдеры
│   │   ├── repositories/    # слой SQL-запросов
│   │   ├── schemas/         # Pydantic-схемы
│   │   ├── services/        # бизнес-логика
│   │   └── utils/           # генерация демо-данных
│   ├── .env.example
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── public/assets/       # иконки и графика
│   ├── src/
│   │   ├── components/      # Vue-компоненты
│   │   ├── pages/           # страницы
│   │   ├── router/          # маршрутизация
│   │   ├── services/        # API-клиент и вспомогательная логика
│   │   └── styles/          # глобальные стили
│   └── Dockerfile
├── docker-compose.yml
├── postman_collection.json
└── README.md
```

## Инструкция запуска

Запуск из корня репозитория:

```bash
docker compose up --build
```

После старта будут доступны:

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- Healthcheck: `http://localhost:8000/health`

Для остановки контейнеров:

```bash
docker compose down
```

Если нужен полностью чистый запуск с пересозданием данных:

```bash
docker compose down -v
docker compose up --build
```

## Описание эндпоинтов

Полная коллекция для проверки API находится в файле [postman_collection.json](postman_collection.json).

Основные эндпоинты backend:

### Пользователи

- `POST /api/v1/users` — создать пользователя и получить JWT
- `POST /api/v1/users/login` — войти по email и паролю
- `GET /api/v1/users/me` — получить профиль текущего пользователя
- `PATCH /api/v1/users/me/profile` — обновить профиль текущего пользователя
- `GET /api/v1/users/{user_id}/token` — получить JWT по id пользователя
- `PATCH /api/v1/users/{user_id}` — изменить имя пользователя
- `DELETE /api/v1/users/{user_id}` — удалить пользователя

### Публикации

- `GET /api/v1/posts/feed?limit=12&offset=0` — получить общую ленту публикаций
- `POST /api/v1/posts` — создать публикацию
- `PATCH /api/v1/posts/{post_id}` — изменить публикацию
- `DELETE /api/v1/posts/{post_id}` — удалить публикацию
- `GET /api/v1/posts/user/{user_id}?limit=10&offset=0` — получить публикации конкретного пользователя

## Что реализовано по ТЗ

### Backend

- создание пользователя с возвратом JWT-токена;
- получение JWT по id пользователя;
- изменение имени пользователя;
- удаление пользователя;
- создание публикации только авторизованным пользователем;
- изменение публикации только автором;
- удаление публикации только автором;
- получение всех публикаций пользователя;
- Redis-кэш публикаций на 10 минут;
- чтение из Postgres с искусственной задержкой 2 секунды при cache miss;
- Dependency Injection через `Depends`;
- параметризованные SQL-запросы без SQLAlchemy.

### Frontend

- страница ленты публикаций на Vue 3;
- карточки постов с `title`, кратким `text` и `created_at`;
- модалка публикации с `title`, `text`, `user_id`, `created_at`, `updated_at`;
- открытие модалки по клику на карточку;
- закрытие по клику на overlay и кнопку закрытия;
- анимация через `Vue Transition`;
- infinite scroll с догрузкой за 500px до конца страницы;
- append-only обновление ленты;
- индикатор загрузки;
- остановка запросов, когда данные закончились;
- переход к публикациям конкретного автора;
- просмотр своих публикаций;
- поиск по заголовку, тексту и имени пользователя.

## Как показать Redis-кэш

Кэш используется для эндпоинта `GET /api/v1/posts/user/{user_id}`.

Сценарий демонстрации:

1. Открыть Postman или Swagger.
2. Выполнить запрос `GET /api/v1/posts/user/{user_id}?limit=10&offset=0`.
3. Первый запрос идет в Postgres и специально ждет около 2 секунд.
4. Повторить тот же запрос сразу еще раз.
5. Повторный ответ должен прийти значительно быстрее, потому что данные уже читаются из Redis.

TTL кэша задается через `CACHE_TTL_SECONDS=600`.

## Как показать использование DI

Dependency Injection реализован через `FastAPI Depends`.

Основная цепочка зависимостей:

- роутер получает сервис через `Depends(...)`;
- сервис получает репозиторий и Redis-клиент через `Depends(...)`;
- репозиторий получает пул Postgres через `Depends(...)`;
- авторизация получает `UserService` через `Depends(...)`.

Ключевые файлы:

- [backend/app/dependencies/services.py](backend/app/dependencies/services.py)
- [backend/app/dependencies/auth.py](backend/app/dependencies/auth.py)
- [backend/app/api/routers/users.py](backend/app/api/routers/users.py)
- [backend/app/api/routers/posts.py](backend/app/api/routers/posts.py)

Это позволяет не создавать сервисы и репозитории вручную внутри роутов и держать слои приложения изолированными.

