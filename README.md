# Trendsee

Fullstack-приложение для работы с лентой публикаций.

Проект реализует backend на FastAPI и frontend на Vue 3: сервис публикаций с JWT-авторизацией, PostgreSQL, Redis-кэшированием и интерфейсом ленты, сверстанным по Figma.

## Реализованная функциональность

### Backend

Реализовано:

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

Реализовано:

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

## Локальный запуск без Docker

### Backend

```bash
cd backend
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

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

## Как проверить обязательные функции

### Через интерфейс

1. Открыть `http://localhost:5173`
2. Зарегистрировать нового пользователя
3. Открыть профиль и убедиться, что доступно изменение имени
4. В профиле нажать `Создать публикацию` и создать новую карточку
5. Открыть карточку и проверить модалку публикации
6. Для своей публикации проверить `Редактировать` и `Удалить`
7. Нажать на сердечко карточки и убедиться, что публикация появляется в разделе `Избранные`
8. Прокрутить страницу вниз и убедиться, что infinite scroll подгружает новые данные

### Через Swagger / Postman

1. Открыть `http://localhost:8000/docs`
2. Проверить `POST /users`
3. Проверить `GET /users/{user_id}/token`
4. Проверить `PATCH /users/{user_id}`
5. Проверить `DELETE /users/{user_id}`
6. Проверить `POST /posts`
7. Проверить `PATCH /posts/{post_id}`
8. Проверить `DELETE /posts/{post_id}`
9. Проверить `GET /posts/user/{user_id}`

## Postman

В корне репозитория лежит готовая коллекция:

- [postman_collection.json](postman_collection.json)

## Архитектурные решения

- backend разделен на слои `api -> services -> repositories -> db`;
- зависимости сервисов и авторизации подключаются через DI;
- Redis используется как горячий кэш публикаций;
- Postgres остается основным источником данных;
- frontend разделен на страницы, компоненты и сервисный слой API;
- ключевой функционал приложения оставлен активным, дополнительные действия из макета переведены в безопасные заглушки.

## Проверка перед сдачей

Команды для финальной проверки:

```bash
cd frontend && npm run build
python -m compileall backend/app
docker compose config
```

При необходимости можно полностью пересоздать окружение:

```bash
docker compose down -v
docker compose up --build
```
