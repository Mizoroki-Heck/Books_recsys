from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv
import os

load_dotenv()

db_host = os.getenv('DB_HOST')
engine = create_engine(db_host, echo=True)


# Base = declarative_base()

# class Book(Base):
#     __tablename__ = 'books'

#     id = Column(Integer, primary_key=True, index=True)
#     Title = Column(String)
#     Author = Column(String)
#     Annotation = Column(Text)
#     genre = Column(String)
#     series = Column(String)
#     book_cover = Column(String)


# Base.metadata.create_all(bind=engine)

def load_to_db(df):
    """Загружает DataFrame в PostgreSQL"""
    df.to_sql('books', con=engine, if_exists='append', index=False)  # Загружаем данные в таблицу 'books'
    print(f"✅ Данные загружены в PostgreSQL!")

