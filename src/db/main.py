from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import ConfigAccessEnvVarriable

engine = AsyncEngine( 
   create_engine(
      url=ConfigAccessEnvVarriable.DATABASE_URL,
      echo=True
))


''' initiate connection to the db'''
async def init_db():
   async with engine.begin() as conn:
      from src.books.models import Book

      await conn.run_sync(SQLModel.metadata.create_all)
