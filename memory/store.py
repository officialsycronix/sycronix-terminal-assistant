import json, sys, os
from datetime import datetime
from pathlib import Path
if __name__ != "__main__":
    _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _root not in sys.path:
        sys.path.insert(0, _root)

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, select
from sqlalchemy.orm import declarative_base, sessionmaker
from core.config import MEMORY_FILE

Base = declarative_base()

class Memory(Base):
    __tablename__ = "memory"
    id = Column(Integer, primary_key=True)
    key = Column(String(255), unique=True, index=True)
    value = Column(Text)
    category = Column(String(100), default="general")
    timestamp = Column(DateTime, default=datetime.utcnow)
    ttl = Column(Integer, nullable=True)

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    role = Column(String(50))
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class MemoryStore:
    def __init__(self):
        self.engine = create_engine(f"sqlite:///{MEMORY_FILE}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def _session(self):
        return self.Session()

    def remember(self, key, value, category="general", ttl=None):
        session = self._session()
        try:
            existing = session.execute(
                select(Memory).where(Memory.key == key)
            ).scalar_one_or_none()
            if existing:
                existing.value = value if isinstance(value, str) else json.dumps(value)
                existing.timestamp = datetime.utcnow()
                existing.ttl = ttl
            else:
                entry = Memory(
                    key=key,
                    value=value if isinstance(value, str) else json.dumps(value),
                    category=category,
                    ttl=ttl,
                )
                session.add(entry)
            session.commit()
        finally:
            session.close()

    def recall(self, key):
        session = self._session()
        try:
            entry = session.execute(
                select(Memory).where(Memory.key == key)
            ).scalar_one_or_none()
            if entry:
                if entry.ttl and (datetime.utcnow() - entry.timestamp).total_seconds() > entry.ttl:
                    session.delete(entry)
                    session.commit()
                    return None
                try:
                    return json.loads(entry.value)
                except:
                    return entry.value
            return None
        finally:
            session.close()

    def forget(self, key):
        session = self._session()
        try:
            entry = session.execute(
                select(Memory).where(Memory.key == key)
            ).scalar_one_or_none()
            if entry:
                session.delete(entry)
                session.commit()
                return True
            return False
        finally:
            session.close()

    def list_category(self, category):
        session = self._session()
        try:
            entries = session.execute(
                select(Memory).where(Memory.category == category)
            ).scalars().all()
            return [{"key": e.key, "value": e.value[:50], "time": str(e.timestamp)[:19]} for e in entries]
        finally:
            session.close()

    def get_count(self):
        session = self._session()
        try:
            return session.query(Memory).count()
        finally:
            session.close()

    def clear(self):
        session = self._session()
        try:
            session.query(Memory).delete()
            session.commit()
        finally:
            session.close()

store = MemoryStore()
