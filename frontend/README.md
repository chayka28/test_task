# Frontend Trendsee

Frontend находится в папке `frontend/` и реализован на Vue 3 + Vite.

## Что есть в интерфейсе

- лента публикаций с infinite scroll;
- модалка публикации с детальной информацией;
- регистрация и вход по JWT;
- профиль пользователя с редактированием имени и аватарки;
- сворачиваемый sidebar и интерактивные UI-заглушки;
- отдельный мобильный маршрут `/mobile-preview`.

## Запуск

Рекомендуемый способ запуска всего проекта:

```bash
docker compose up --build
```

Локальный запуск только frontend:

```bash
cd frontend
npm install
npm run dev
```

## Важные директории

- `src/components` — переиспользуемые Vue-компоненты
- `src/pages` — страницы приложения
- `src/router` — маршрутизация
- `src/services` — API-клиент, localStorage, форматирование
- `src/styles` — глобальные стили

Подробное описание проекта и backend API находится в корневом [README.md](../README.md).
