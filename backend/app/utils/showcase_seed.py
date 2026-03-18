from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from app.utils.demo_posts import build_demo_posts

SHOWCASE_AUTHORS = [
    ("Alexandra", "alexandra@trendsee.local", "Beauty"),
    ("Maria", "maria@trendsee.local", "Marketing"),
    ("Anna", "anna@trendsee.local", "Education"),
    ("Polina", "polina@trendsee.local", "Content"),
    ("Daria", "daria@trendsee.local", "Expert"),
    ("Sofia", "sofia@trendsee.local", "Sales"),
    ("Valeria", "valeria@trendsee.local", "Reels"),
    ("Ekaterina", "ekaterina@trendsee.local", "Lead Magnet"),
    ("Alina", "alina@trendsee.local", "Personal Brand"),
    ("Veronika", "veronika@trendsee.local", "Strategy"),
    ("Tatiana", "tatiana@trendsee.local", "Creative"),
    ("Olga", "olga@trendsee.local", "Funnel"),
    ("Natalia", "natalia@trendsee.local", "Editing"),
    ("Yulia", "yulia@trendsee.local", "Triggers"),
    ("Elena", "elena@trendsee.local", "Scripts"),
    ("Irina", "irina@trendsee.local", "Reach"),
    ("Ksenia", "ksenia@trendsee.local", "Promotion"),
    ("Victoria", "victoria@trendsee.local", "Analytics"),
    ("Anastasia", "anastasia@trendsee.local", "Expert"),
    ("Diana", "diana@trendsee.local", "Niche"),
    ("Kristina", "kristina@trendsee.local", "Loyalty"),
    ("Milana", "milana@trendsee.local", "Content Plan"),
    ("Arina", "arina@trendsee.local", "Ads"),
    ("Ulyana", "ulyana@trendsee.local", "Presentation"),
    ("Eva", "eva@trendsee.local", "Product"),
    ("Nika", "nika@trendsee.local", "Packaging"),
    ("Liza", "liza@trendsee.local", "Copywriting"),
    ("Karina", "karina@trendsee.local", "Cases"),
    ("Yana", "yana@trendsee.local", "Formats"),
    ("Alyona", "alyona@trendsee.local", "Insights"),
]

POSTS_PER_AUTHOR = 3


async def ensure_showcase_feed(
    user_repository: UserRepository,
    post_repository: PostRepository,
) -> None:
    for index, (name, email, focus) in enumerate(SHOWCASE_AUTHORS):
        auth_user = await user_repository.get_auth_payload_by_email(email=email)

        if auth_user is None:
            user = await user_repository.create_user(name=name, email=email)
        else:
            user = await user_repository.get_by_id(user_id=auth_user["id"])

        if user is None:
            continue

        existing_count = await post_repository.count_user_posts(user_id=user["id"])
        if existing_count >= POSTS_PER_AUTHOR:
            continue

        missing_count = POSTS_PER_AUTHOR - existing_count
        demo_posts = build_demo_posts(
            start_index=index * POSTS_PER_AUTHOR + existing_count,
            count=missing_count,
        )

        for post in demo_posts:
            await post_repository.create_post(
                user_id=user["id"],
                title=f"{focus}: {post['title']}",
                text=post["text"],
                video_url=post.get("video_url"),
                poster_url=post.get("poster_url"),
                source_url=post.get("source_url"),
            )
