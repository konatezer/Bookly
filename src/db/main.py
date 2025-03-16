from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker


from src.config import ConfigAccessEnvVarriable

async_engine = AsyncEngine( 
   create_engine(
      url=ConfigAccessEnvVarriable.DATABASE_URL,
      echo=True
))


''' initiate connection to the db'''
async def init_db():
   async with async_engine.begin() as conn:
      await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
   SessionLocal = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


   async with SessionLocal() as session:
      yield session