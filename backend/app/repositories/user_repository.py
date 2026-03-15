import asyncpg


class UserRepository:
    def __init__(self, pool: asyncpg.Pool) -> None:
        self.pool = pool

    async def create_user(self, name: str) -> dict:
        # All queries use placeholders ($1, $2, ...) to avoid SQL injection.
        query = """
            INSERT INTO users (name)
            VALUES ($1)
            RETURNING id, name, created_at, updated_at
        """
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(query, name)
        return dict(row)

    async def get_by_id(self, user_id: int) -> dict | None:
        query = """
            SELECT id, name, created_at, updated_at
            FROM users
            WHERE id = $1
        """
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(query, user_id)
        return dict(row) if row else None

    async def update_name(self, user_id: int, name: str) -> dict | None:
        query = """
            UPDATE users
            SET name = $2, updated_at = NOW()
            WHERE id = $1
            RETURNING id, name, created_at, updated_at
        """
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(query, user_id, name)
        return dict(row) if row else None

    async def delete_user(self, user_id: int) -> bool:
        query = "DELETE FROM users WHERE id = $1"
        async with self.pool.acquire() as connection:
            result = await connection.execute(query, user_id)
        return result == "DELETE 1"
