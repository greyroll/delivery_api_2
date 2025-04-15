from contextlib import contextmanager
from pathlib import Path

from sqlmodel import SQLModel, create_engine, Session

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

class BaseORMManager:
	model: SQLModel | None = None

	def __init__(self):
		project_root = Path(__file__).resolve().parent.parent  # 1 уровня вверх от текущего файла
		db_path = project_root / "delivery.db"  # Путь к базе данных в корне проекта

		self.engine = create_engine(f"sqlite:///{db_path}")

	@contextmanager
	def session_scope(self):
		session = Session(self.engine)
		try:
			yield session
			session.commit()
		except Exception:
			session.rollback()
			raise
		finally:
			session.close()

	def create_all_tables(self):
		SQLModel.metadata.create_all(self.engine)

	def add(self, obj: SQLModel):
		with self.session_scope() as session:
			session.add(obj)
			session.commit()
			session.refresh(obj)

	def add_all(self, objs: list[SQLModel]):
		with self.session_scope() as session:
			session.add_all(objs)
			session.commit()
			session.refresh(objs)

	def delete(self, obj_id: int):
		with self.session_scope() as session:
			obj = session.get(self.model, obj_id)
			session.delete(obj)
			session.commit()

