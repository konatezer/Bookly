import redis.asyncio as aioredis

from src.config import ConfigAccessEnvVarriable

JTI_EXPIRY = 3600

token_blocklist = aioredis.from_url(ConfigAccessEnvVarriable.REDIS_URL)


async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)


async def token_in_blocklist(jti: str) -> bool:
    jti = await token_blocklist.get(jti)

    return jti is not None


# Admin
[
    "adding users",
    "change role",
    "crud on users",
    "submit book",
    "crud on reviews",
    "revoking access",
]

# users
[
    "crud on thier own book submission",
    "crud on thier own review",
    "crud on thier own account",
]
