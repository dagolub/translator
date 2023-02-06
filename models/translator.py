from sqlalchemy import Column, String  # type: ignore

from db.base_class import Base


class Translator(Base):
    __tablename__: str = "translator_text"  # type: ignore
    _id = Column(String, primary_key=True, index=True)
    text = Column(String)
    text_translated = Column(String)
    status = Column(String)
