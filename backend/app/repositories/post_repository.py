import asyncpg


class PostRepository:
    def __init__(self, pool: asyncpg.Pool) -> None:
        self.pool = pool

    async def create_post(self, user_id: int, title: str, text: str) -> dict:
        # Parameterized SQL keeps this layer safe for external input.
        query = """
            INSERT INTO posts (user_id, title, text)
            VALUES ($1, $2, $3)
            RETURNING id, user_id, title, text, created_at, updated_at
        """
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(query, user_id, title, text)
        return dict(row)

    async def get_by_id(self, post_id: int) -> dict | None:
        query = """
            SELECT id, user_id, title, text, created_at, updated_at
            FROM posts
            WHERE id = $1
        """
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(query, post_id)
        return dict(row) if row else None

    async def get_user_posts(self, user_id: int) -> list[dict]:
        query = """
            SELECT id, user_id, title, text, created_at, updated_at
            FROM posts
            WHERE user_id = $1
            ORDER BY created_at DESC
        """
        async with self.pool.acquire() as connection:
            rows = await connection.fetch(query, user_id)
        return [dict(row) for row in rows]

    async def count_user_posts(self, user_id: int) -> int:
        query = """
            SELECT COUNT(*)
            FROM posts
            WHERE user_id = $1
        """
        async with self.pool.acquire() as connection:
            value = await connection.fetchval(query, user_id)
        return int(value or 0)

    async def update_post(
        self,
        post_id: int,
        title: str | None,
        text: str | None,
    ) -> dict | None:
        query = """
            UPDATE posts
            SET
                title = COALESCE($2, title),
                text = COALESCE($3, text),
                updated_at = NOW()
            WHERE id = $1
            RETURNING id, user_id, title, text, created_at, updated_at
        """
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(query, post_id, title, text)
        return dict(row) if row else None

    async def delete_post(self, post_id: int) -> dict | None:
        query = """
            DELETE FROM posts
            WHERE id = $1
            RETURNING id, user_id, title, text, created_at, updated_at
        """
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(query, post_id)
        return dict(row) if row else None
