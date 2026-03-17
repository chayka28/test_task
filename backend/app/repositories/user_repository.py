import asyncpg


class UserRepository:
    def __init__(self, pool: asyncpg.Pool) -> None:
        self.pool = pool

    async def create_user(
        self,
        name: str,
        email: str | None = None,
        password_hash: str | None = None,
        avatar_data: str | None = None,
    ) -> dict:
        # Все запросы используют placeholders, чтобы не допускать SQL injection.
        query = """
            INSERT INTO users (name, email, password_hash, avatar_data)
            VALUES ($1, $2, $3, $4)
            RETURNING id, name, email, avatar_data, created_at, updated_at
        """
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(query, name, email, password_hash, avatar_data)
        return dict(row)

    async def get_by_id(self, user_id: int) -> dict | None:
        query = """
            SELECT id, name, email, avatar_data, created_at, updated_at
            FROM users
            WHERE id = $1
        """
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(query, user_id)
        return dict(row) if row else None

    async def get_auth_payload_by_email(self, email: str) -> dict | None:
        query = """
            SELECT id, name, email, avatar_data, password_hash, created_at, updated_at
            FROM users
            WHERE email = $1
            LIMIT 1
        """
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(query, email)
        return dict(row) if row else None

    async def get_by_name(self, name: str) -> dict | None:
        query = """
            SELECT id, name, email, avatar_data, created_at, updated_at
            FROM users
            WHERE name = $1
            ORDER BY id ASC
            LIMIT 1
        """
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(query, name)
        return dict(row) if row else None

    async def update_name(self, user_id: int, name: str) -> dict | None:
        query = """
            UPDATE users
            SET name = $2, updated_at = NOW()
            WHERE id = $1
            RETURNING id, name, email, avatar_data, created_at, updated_at
        """
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(query, user_id, name)
        return dict(row) if row else None

    async def update_profile(
        self,
        user_id: int,
        name: str | None = None,
        avatar_data: str | None = None,
    ) -> dict | None:
        query = """
            UPDATE users
            SET
                name = COALESCE($2, name),
                avatar_data = COALESCE($3, avatar_data),
                updated_at = NOW()
            WHERE id = $1
            RETURNING id, name, email, avatar_data, created_at, updated_at
        """
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow(query, user_id, name, avatar_data)
        return dict(row) if row else None

    async def delete_user(self, user_id: int) -> bool:
        query = "DELETE FROM users WHERE id = $1"
        async with self.pool.acquire() as connection:
            result = await connection.execute(query, user_id)
        return result == "DELETE 1"
