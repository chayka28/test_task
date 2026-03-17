# Trendsee

Fullstack-приложение для работы с лентой публикаций.

Проект реализует backend на FastAPI и frontend на Vue 3: сервис публикаций с JWT-авторизацией, PostgreSQL, Redis-кэшированием и интерфейсом ленты, сверстанным по Figma.

## Реализованная функциональность

### Backend

- создание пользователя с возвратом JWT;
- получение JWT по `user_id` для тестирования;
- изменение имени пользователя;
- удаление пользователя;
- создание публикации только авторизованным пользователем;
- изменение публикации;
- удаление публикации;
- получение всех публикаций пользователя;
- поддержка дополнительных media-полей публикации: `video_url`, `poster_url`, `source_url`;
- Redis-кэш публикаций на 10 минут;
- чтение из Postgres с искусственной задержкой `2s`, если кэш пустой или устарел;
- Dependency Injection через `Depends`;
- параметризованные SQL-запросы без SQLAlchemy.

### Frontend

- лента публикаций, получаемая с backend;
- карточка публикации с `title`, кратким `text` и `created_at`;
- модальное окно публикации с `title`, `text`, `user_id`, `created_at`, `updated_at`;
- открытие модалки по клику на карточку;
- закрытие модалки по overlay и кнопке закрытия;
- анимация открытия и закрытия через `Vue Transition`;
- infinite scroll за `500px` до конца страницы;
- append-only догрузка данных без перезаписи уже загруженных карточек;
- индикатор загрузки при первом запросе и при догрузке;
- остановка запросов, если публикаций больше нет.

## Дополнительно

Для удобства демонстрации добавлены:

- регистрация и вход по `email + password`;
- профиль пользователя как отдельная модалка;
- создание, редактирование и удаление публикаций через интерфейс;
- публикации с дополнительными полями для видео, превью и внешнего источника;
- раздел `Избранные` с сохранением публикаций;
- кнопка `Найти еще ролики` с реальной догрузкой контента;
- раскрывающийся блок `Creative +`;
- демонстрационный публичный режим для просмотра интерфейса без входа.

Элементы интерфейса из макета, которые пока не реализованы как отдельные продуктовые модули, оставлены как неактивные заглушки с уведомлением `Функция недоступна`.

## Технологии

### Backend

- Python 3.12
- FastAPI
- asyncpg
- Redis
- PostgreSQL
- python-jose
- passlib

### Frontend

- Vue 3
- Vite
- Vue Router

### Инфраструктура

- Docker
- Docker Compose

## Структура проекта

```text
.
├── backend/
│   ├── app/
│   │   ├── api/             # HTTP-роуты
│   │   ├── core/            # конфигурация и безопасность
│   │   ├── db/              # Postgres, Redis, init.sql
│   │   ├── dependencies/    # DI-провайдеры
│   │   ├── repositories/    # SQL-слой
│   │   ├── schemas/         # Pydantic-схемы
│   │   ├── services/        # бизнес-логика
│   │   └── utils/           # генерация демонстрационных публикаций
│   ├── .env.example
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── public/assets/       # иконки и графика
│   ├── src/
│   │   ├── components/      # Vue-компоненты
│   │   ├── pages/           # страницы
│   │   ├── router/          # роутер
│   │   ├── services/        # API, local state, форматирование
│   │   └── styles/          # глобальные стили
│   └── Dockerfile
├── docker-compose.yml
├── postman_collection.json
└── README.md
```

## Запуск проекта

Из корня репозитория:

```bash
docker compose up --build
```

После запуска доступны:

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- Healthcheck: `http://localhost:8000/health`

## Переменные окружения

Пример конфигурации: [backend/.env.example](backend/.env.example)

Основные переменные:

- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `REDIS_URL`
- `CACHE_TTL_SECONDS=600`
- `JWT_SECRET`
- `JWT_ALGORITHM`
- `JWT_EXPIRE_MINUTES`

## API

Префикс: `/api/v1`

### Пользователи

- `GET /users/demo` — демонстрационный пользователь для публичной ленты
- `POST /users` — создать пользователя и получить JWT
- `POST /users/login` — вход по email и паролю
- `GET /users/me` — профиль текущего пользователя
- `PATCH /users/me/profile` — обновить профиль текущего пользователя
- `GET /users/{user_id}/token` — получить JWT по id пользователя
- `PATCH /users/{user_id}` — изменить имя пользователя
- `DELETE /users/{user_id}` — удалить пользователя

### Публикации

- `POST /posts` — создать публикацию
- `PATCH /posts/{post_id}` — изменить публикацию
- `DELETE /posts/{post_id}` — удалить публикацию
- `GET /posts/user/{user_id}?limit=10&offset=0` — получить публикации пользователя
- `POST /posts/demo-seed?count=12&append=false` — сгенерировать демонстрационные публикации
- `POST /posts/demo-seed/public?count=12&append=true` — догрузить публикации в публичную ленту
