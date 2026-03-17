# Frontend

Frontend реализован на Vue 3 + Vite и работает поверх FastAPI из этого же репозитория.

## Что есть в интерфейсе

- лента публикаций с infinite scroll;
- детальная модалка публикации;
- регистрация через JWT;
- сохранение сессии и избранного в `localStorage`;
- сворачиваемый sidebar;
- раскрытие блока `Creative +`;
- интерактивные заглушки для вторичных действий;
- отдельный мобильный экран `/mobile-preview`.

## Запуск

Рекомендуемый способ:

```bash
docker compose up --build
```

Адреса:

- `http://localhost:5173/` — основная страница
- `http://localhost:5173/mobile-preview` — мобильный референс

## Локальный запуск frontend

```bash
cd frontend
npm install
npm run dev
```

Vite proxy уже настроен:

- `/api` -> `http://localhost:8000`
- `/health` -> `http://localhost:8000`

## Структура `src`

- `pages/` — страницы приложения
- `components/` — UI-компоненты
- `services/` — API, форматирование и локальное состояние
- `router/` — маршруты
- `styles/` — глобальные стили
