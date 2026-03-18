from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from app.utils.demo_posts import build_demo_posts

SHOWCASE_CREATORS = [
    ("Александра Романова", "creator01@trendsee.demo", "Контент-стратегия"),
    ("Ника Белова", "creator02@trendsee.demo", "Бьюти-контент"),
    ("Дарья Орехова", "creator03@trendsee.demo", "Личный бренд"),
    ("Антон Ларионов", "creator04@trendsee.demo", "Маркетинг"),
    ("Мария Громова", "creator05@trendsee.demo", "Продажи"),
    ("Валерия Мельник", "creator06@trendsee.demo", "Экспертные Reels"),
    ("Ольга Шестакова", "creator07@trendsee.demo", "Креативы"),
    ("Екатерина Воронова", "creator08@trendsee.demo", "Монтаж"),
    ("Ирина Ковалева", "creator09@trendsee.demo", "Копирайтинг"),
    ("Юлия Тарасова", "creator10@trendsee.demo", "Тренды"),
    ("Павел Нестеров", "creator11@trendsee.demo", "Аналитика"),
    ("Максим Елисеев", "creator12@trendsee.demo", "Инфопродукты"),
    ("София Лукина", "creator13@trendsee.demo", "SMM"),
    ("Алина Жукова", "creator14@trendsee.demo", "UGC"),
    ("Ксения Лебедева", "creator15@trendsee.demo", "Фриланс"),
    ("Виктория Панова", "creator16@trendsee.demo", "Продюсирование"),
    ("Кира Демидова", "creator17@trendsee.demo", "Дизайн"),
    ("Арина Осипова", "creator18@trendsee.demo", "Сторителлинг"),
    ("Егор Баженов", "creator19@trendsee.demo", "Запуски"),
    ("Леонид Миронов", "creator20@trendsee.demo", "Сценарии"),
    ("Ева Савина", "creator21@trendsee.demo", "Контент-план"),
    ("Анастасия Мартынова", "creator22@trendsee.demo", "Обзоры"),
    ("Полина Яковлева", "creator23@trendsee.demo", "Психология продаж"),
    ("Тимур Грачев", "creator24@trendsee.demo", "Трафик"),
    ("Вероника Крылова", "creator25@trendsee.demo", "Позиционирование"),
    ("Станислав Фомин", "creator26@trendsee.demo", "YouTube Shorts"),
    ("Лилия Ермакова", "creator27@trendsee.demo", "Распаковка продукта"),
    ("Таисия Рябова", "creator28@trendsee.demo", "Обучающий контент"),
    ("Никита Седов", "creator29@trendsee.demo", "Автоворонки"),
    ("Ульяна Гордеева", "creator30@trendsee.demo", "Нишевые видео"),
]

POSTS_PER_CREATOR = 3


async def ensure_showcase_feed(
    user_repository: UserRepository,
    post_repository: PostRepository,
) -> None:
    """Создает витринных авторов и стартовый набор публикаций для демо-ленты."""

    for creator_index, (name, email, focus) in enumerate(SHOWCASE_CREATORS):
        user = await user_repository.get_by_email(email=email)
        if user is None:
            user = await user_repository.create_user(
                name=name,
                email=email,
                password_hash=None,
                avatar_data=None,
            )

        existing_posts = await post_repository.count_user_posts(user_id=user["id"])
        if existing_posts >= POSTS_PER_CREATOR:
            continue

        missing_posts = POSTS_PER_CREATOR - existing_posts
        start_index = creator_index * POSTS_PER_CREATOR + existing_posts
        demo_posts = build_demo_posts(start_index=start_index, count=missing_posts)

        for post in demo_posts:
            await post_repository.create_post(
                user_id=user["id"],
                title=f"{focus}: {post['title']}",
                text=post["text"],
                video_url=post.get("video_url"),
                poster_url=post.get("poster_url"),
                source_url=post.get("source_url"),
            )
