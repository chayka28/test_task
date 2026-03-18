# Trendsee

Trendsee — fullstack-приложение для просмотра и управления лентой публикаций.

Стек проекта:
- backend: `FastAPI`, `PostgreSQL`, `Redis`, `asyncpg`, `JWT`
- frontend: `Vue 3`, `Vite`, `Vue Router`
- инфраструктура: `Docker`, `docker compose`

После запуска проект автоматически наполняется демонстрационными данными: создаются витринные авторы и публикации, поэтому интерфейс сразу выглядит как рабочий продукт и подходит для демонстрации.

## Краткое описание структуры проекта

```text
.
├── backend/
│   ├── app/
│   │   ├── api/             # HTTP-роуты FastAPI
│   │   ├── core/            # конфигурация, security, JWT
│   │   ├── db/              # подключение к Postgres/Redis, init.sql
│   │   ├── dependencies/    # Dependency Injection через Depends
│   │   ├── repositories/    # SQL-слой и доступ к данным
│   │   ├── schemas/         # Pydantic-схемы запросов и ответов
│   │   ├── services/        # бизнес-логика пользователей и публикаций
│   │   └── utils/           # генерация демонстрационных данных
│   ├── .env.example
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── public/assets/       # иконки и статические ассеты
│   ├── src/
│   │   ├── components/      # интерфейсные компоненты
│   │   ├── pages/           # страницы приложения
│   │   ├── router/          # маршрутизация
│   │   ├── services/        # работа с API, local state, форматирование
│   │   └── styles/          # глобальные стили
│   ├── Dockerfile
│   └── nginx.conf
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
- frontend: `http://localhost:5173`
- backend API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- healthcheck: `http://localhost:8000/health`

Если нужно полностью пересоздать окружение и данные:

```bash
docker compose down -v
docker compose up --build
```

## Описание эндпоинтов

Готовая коллекция лежит в корне проекта:
- [postman_collection.json](postman_collection.json)

Префикс API:
- `/api/v1`

### Пользователи
- `POST /users` — создание пользователя с возвратом JWT
- `POST /users/login` — вход по email и паролю
- `GET /users/me` — текущий профиль пользователя
- `PATCH /users/me/profile` — обновление текущего профиля
- `GET /users/{user_id}/token` — получение JWT по id пользователя
- `PATCH /users/{user_id}` — изменение имени пользователя
- `DELETE /users/{user_id}` — удаление пользователя
- `GET /users/demo` — служебный demo-user для публичных сценариев

### Публикации
- `GET /posts/feed?limit=12&offset=0` — общая витринная лента публикаций
- `POST /posts` — создание публикации авторизованным пользователем
- `PATCH /posts/{post_id}` — редактирование публикации автором
- `DELETE /posts/{post_id}` — удаление публикации автором
- `GET /posts/user/{user_id}?limit=10&offset=0` — публикации конкретного пользователя
- `POST /posts/demo-seed?count=12&append=false` — генерация стартовых публикаций для текущего пользователя
- `POST /posts/demo-seed/public?count=12&append=true` — догенерация demo-контента для публичных сценариев

## Что реализовано

### Backend
- JWT-авторизация
- создание, изменение и удаление пользователей
- создание, изменение и удаление публикаций
- получение публикаций пользователя
- Redis-кэш для публикаций пользователя на 10 минут
- fallback в Postgres с искусственной задержкой `2 секунды`
- Dependency Injection через `Depends`
- параметризованные SQL-запросы

### Frontend
- лента публикаций на Vue 3
- infinite scroll с догрузкой за `500px` до конца страницы
- карточки публикаций с датой, заголовком и кратким текстом
- модальное окно публикации с полной информацией
- `Vue Transition` для модальных окон
- регистрация и вход
- профиль пользователя
- создание, редактирование и удаление собственных публикаций
- избранное
- фильтрация и поиск по ленте
- демонстрационная витрина из нескольких авторов

## Как быстро показать проект в скринкасте

Ниже удобный сценарий обзорного показа на 3–5 минут.

### 1. Старт проекта
Показать запуск:

```bash
docker compose up --build
```

Коротко сказать:
- backend и frontend поднимаются одной командой
- PostgreSQL хранит данные
- Redis используется для кэширования публикаций пользователя
- после старта проект уже заполнен демонстрационным контентом

### 2. Главная страница
Показать:
- боковое меню
- верхний блок поиска
- витринную ленту публикаций
- infinite scroll
- фильтры и поиск

Коротко пояснить:
- главная лента работает как продуктовая витрина
- в базе уже есть несколько десятков авторов и публикаций
- можно прокручивать, фильтровать, открывать подробный разбор публикации

### 3. Модалка публикации
Открыть любую карточку и показать:
- полную информацию о публикации
- транскрибацию
- блоки с сутью, структурой и рабочими приемами
- закрытие по overlay и по кнопке

### 4. Авторизация и работа со своими публикациями
Показать:
- регистрацию нового пользователя
- вход в аккаунт
- профиль
- создание новой публикации
- редактирование своей публикации
- удаление своей публикации

Отдельно можно отметить:
- чужие публикации редактировать и удалять нельзя
- backend дополнительно защищает это ограничение на уровне API

### 5. Избранное
Показать:
- добавление публикации в избранное
- переход в раздел `Избранные`
- отображение сохраненных карточек

## Как показать Redis-кэш работодателю

Даже без внешних реальных источников Redis можно показать очень наглядно.

### Вариант через Swagger
1. Открыть `http://localhost:8000/docs`
2. Сначала вызвать `GET /posts/feed?limit=1&offset=0`
3. Взять `user_id` из первой публикации
4. Затем дважды подряд вызвать `GET /posts/user/{user_id}`

Что произойдет:
- первый запрос пойдет в `Postgres` и из-за симуляции нагрузки займет примерно `2 секунды`
- второй запрос придет почти мгновенно, потому что данные уже лежат в `Redis`

### Вариант через PowerShell
Можно показать то же самое замером времени:

```powershell
$uid = 1
Measure-Command { Invoke-RestMethod "http://localhost:8000/api/v1/posts/user/$uid?limit=10&offset=0" | Out-Null }
Measure-Command { Invoke-RestMethod "http://localhost:8000/api/v1/posts/user/$uid?limit=10&offset=0" | Out-Null }
```

Для демонстрации достаточно проговорить:
- первый запрос медленный, потому что идет в Postgres с искусственной задержкой
- второй запрос быстрый, потому что уже читается из Redis

## Как показать DI работодателю

Dependency Injection в проекте реализован через `FastAPI Depends`.

Где это видно в коде:
- `backend/app/api/routers/users.py`
- `backend/app/api/routers/posts.py`
- `backend/app/dependencies/services.py`
- `backend/app/dependencies/auth.py`

Как работает цепочка зависимостей:
- роут не создает сервис вручную, а получает его через `Depends(get_user_service)` или `Depends(get_post_service)`
- провайдер сервиса сам получает зависимости через `Depends`, например репозиторий и Redis-клиент
- провайдер репозитория получает подключение к Postgres через `Depends(get_db_pool)`
- auth-зависимость `get_current_user_id` получает `UserService` через `Depends(get_user_service)` и валидирует JWT

На примере публикаций цепочка выглядит так:
- роут `POST /posts` в `backend/app/api/routers/posts.py`
- получает `current_user_id = Depends(get_current_user_id)`
- получает `post_service = Depends(get_post_service)`
- `get_post_service` в `backend/app/dependencies/services.py`
- получает `post_repository = Depends(get_post_repository)` и `redis_client = Depends(get_redis_client)`
- `get_post_repository` получает `pool = Depends(get_db_pool)`

Что важно проговорить на защите:
- HTTP-слой не знает, как создавать сервисы, репозитории, Redis и Postgres-подключение
- зависимости собираются централизованно в `dependencies`
- благодаря этому слои разделены чище: `router -> service -> repository`
- такой подход упрощает сопровождение, замену реализаций и расширение проекта

Короткий сценарий показа:
1. Открыть `backend/app/api/routers/posts.py` и показать `Depends(get_post_service)` и `Depends(get_current_user_id)`.
2. Открыть `backend/app/dependencies/services.py` и показать, как `PostService` собирается из `PostRepository` и `Redis`.
3. Открыть `backend/app/dependencies/auth.py` и показать, как JWT-пользователь подмешивается в защищенные роуты.
4. Коротко пояснить, что сервисы и репозитории не создаются вручную внутри эндпоинтов.

## Дополнительная проверка перед отправкой

```bash
cd frontend && npm run build
python -m compileall backend/app
docker compose config
```

## Итог

Проект готов к демонстрации как полноценный продуктовый прототип:
- backend закрывает обязательный CRUD, JWT, Redis-кэш и DI
- frontend показывает рабочую ленту, модалки, авторизацию, профиль и взаимодействие с публикациями
- репозиторий уже содержит README, docker compose запуск и Postman-коллекцию
