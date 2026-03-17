# Trendsee

Полноценный fullstack-проект на FastAPI и Vue 3 для работы с лентой публикаций: backend с JWT-авторизацией, PostgreSQL, Redis и frontend, сверстанный по Figma-макету.

## Кратко о проекте

Проект разделен на две независимые части:

- `backend/` — FastAPI, PostgreSQL, Redis, JWT, DI
- `frontend/` — Vue 3, Vite, интерфейс ленты публикаций

## Что реализовано

### Backend

- создание пользователя с немедленной выдачей JWT;
- вход по `email + password`;
- получение токена по `user_id` для удобного тестирования;
- получение и обновление профиля текущего пользователя;
- изменение имени и удаление пользователя;
- создание, изменение и удаление публикаций только авторизованным пользователем;
- получение публикаций пользователя с кэшированием в Redis на 10 минут;
- fallback в Postgres с искусственной задержкой `2s`, если кэш пустой или устарел;
- Dependency Injection через `Depends` для сервисов, репозиториев и авторизации;
- параметризованные SQL-запросы без SQLAlchemy;
- runtime-миграция пользовательской таблицы при старте, чтобы проект поднимался даже на существующем volume.

### Frontend

- лента публикаций на Vue 3;
- infinite scroll с догрузкой за 500px до конца страницы;
- карточки публикаций с заголовком, кратким текстом и датой;
- модалка публикации с полными данными (`title`, `text`, `user_id`, `created_at`, `updated_at`);
- `Vue Transition` для модальных окон и toast-уведомлений;
- регистрация и вход прямо из интерфейса;
- профиль пользователя как отдельная модалка с возможностью смены имени и аватарки;
- избранное и расширенные действия доступны только после авторизации;
- сворачиваемое боковое меню и дополнительные UI-заглушки для сценарного взаимодействия с сайтом;
- отдельная мобильная страница-референс `/mobile-preview`.

## Стек

- Backend: FastAPI, asyncpg, Redis, python-jose
- Frontend: Vue 3, Vue Router, Vite
- Инфраструктура: PostgreSQL, Redis, Docker, Docker Compose

## Структура проекта

```text
.
├── backend/
│   ├── app/
│   │   ├── api/             # HTTP-роуты
│   │   ├── core/            # конфиг и безопасность
│   │   ├── db/              # подключение к Postgres/Redis и init.sql
│   │   ├── dependencies/    # DI-провайдеры
│   │   ├── repositories/    # SQL-доступ к данным
│   │   ├── schemas/         # Pydantic-схемы
│   │   ├── services/        # бизнес-логика
│   │   └── utils/           # генерация демо-контента
│   ├── .env.example
│   └── Dockerfile
├── frontend/
│   ├── public/assets/       # иконки и статические ассеты
│   ├── src/
│   │   ├── components/      # Vue-компоненты
│   │   ├── pages/           # страницы
│   │   ├── router/          # маршрутизация
│   │   ├── services/        # API, форматирование, localStorage
│   │   └── styles/          # глобальные стили
│   └── Dockerfile
├── docker-compose.yml
├── postman_collection.json
└── README.md
```

## Запуск одной командой

Из корня репозитория:

```bash
docker compose up --build
```

После старта будут доступны:

- frontend: `http://localhost:5173`
- backend: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- healthcheck: `http://localhost:8000/health`

## Быстрая проверка

1. Открыть `http://localhost:5173`
2. Зарегистрировать нового пользователя через интерфейс
3. Убедиться, что после входа доступны избранное, профиль и дополнительные действия
4. Открыть модалку публикации по клику на карточку
5. Прокрутить страницу вниз и проверить догрузку карточек
6. Открыть `http://localhost:8000/docs` и при необходимости проверить backend-эндпоинты через Swagger

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

## Переменные окружения backend

Пример лежит в [backend/.env.example](backend/.env.example).

Основные переменные:

- `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
- `REDIS_URL`
- `CACHE_TTL_SECONDS=600`
- `JWT_SECRET`, `JWT_ALGORITHM`, `JWT_EXPIRE_MINUTES`

## Как устроен источник публикаций

По условиям тестового задания внешний video API не требуется. Источник карточек в проекте — это публикации в Postgres.

Сценарий работы:

1. гость открывает сайт и получает открытую демо-ленту;
2. после регистрации или входа пользователь работает уже со своей лентой;
3. дополнительные пачки контента генерируются backend-ом через `demo-seed`, чтобы можно было полноценно показать интерфейс и infinite scroll;
4. frontend строит карточки и модалки исключительно из API-данных.

## Основные API-эндпоинты

Префикс API: `/api/v1`

### Пользователи

- `GET /users/demo` — получить пользователя открытой демо-ленты
- `POST /users` — зарегистрировать пользователя и получить JWT
- `POST /users/login` — войти по email и паролю
- `GET /users/me` — получить профиль текущего пользователя
- `PATCH /users/me/profile` — обновить имя и аватарку текущего пользователя
- `GET /users/{user_id}/token` — получить JWT по id пользователя
- `PATCH /users/{user_id}` — изменить имя пользователя
- `DELETE /users/{user_id}` — удалить пользователя

### Публикации

- `POST /posts` — создать публикацию
- `PATCH /posts/{post_id}` — изменить публикацию
- `DELETE /posts/{post_id}` — удалить публикацию
- `GET /posts/user/{user_id}?limit=10&offset=0` — получить ленту пользователя
- `POST /posts/demo-seed?count=8&append=true` — добавить новую пачку демо-публикаций для текущего пользователя

## Postman

Актуальная коллекция лежит в корне проекта:

- [postman_collection.json](postman_collection.json)

В ней есть сценарии для регистрации, входа, профиля, CRUD пользователей и CRUD публикаций.

## Что важно по ТЗ

- `docker compose up --build` поднимает весь сервис;
- Redis используется как горячий кэш публикаций на 10 минут;
- при чтении мимо кэша используется Postgres и `asyncio.sleep(2)`;
- DI реализован через `Depends`;
- frontend написан на Vue и находится целиком в `frontend/`;
- карточки открывают модалку с полными данными;
- infinite scroll реализован без перезаписи уже загруженных данных.

## Что было дополнительно проверено

Перед финальной упаковкой проекта были отдельно проверены:

- production-сборка frontend;
- компиляция backend-кода;
- валидность `docker compose`;
- валидность Postman-коллекции;
- живой smoke-тест API: регистрация, вход, получение профиля, CRUD публикации, обновление профиля, выдача токена по `user_id`, удаление пользователя;
- поведение кэша публикаций: первый запрос идет через Postgres с задержкой около `2s`, повторный — из Redis за миллисекунды.

## Проверка перед сдачей

Команды, которые были прогнаны перед финальной упаковкой проекта:

```bash
cd frontend && npm run build
python -m compileall backend/app
docker compose config
docker compose up -d --build
```

## Примечание

Если проект уже запускался на старом Docker volume и вы хотите проверить сценарий “с нуля”, можно выполнить:

```bash
docker compose down -v
docker compose up --build
```

## Дополнительно

- Проект расширен относительно базового ТЗ: добавлены вход, профиль, аватарки и дополнительные UI-сценарии.
- Эти доработки не конфликтуют с заданием и не ломают обязательную архитектуру.
