import os
import csv

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Serial
from sqlalchemy.orm import scoped_session, sessionmaker

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
db = scoped_session(sessionmaker(bind=engine)) 
# meta = MetaData()
# students = Table(
#    'books', meta, 
#    Column('id', Integer, primary_key = True), 
#    Column('name', String), 
#    Column('lastname', String),
# )
# meta.create_all(engine)

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    isbn VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER NOT NULL
);

def main():
    fil = open("books.csv")
    read = csv.reader(fil)
    for isbn, title, author, year in read: 
        db.execute("INSERT INTO books(isbn, title, author, year) VALUES (:i, :t, :a, :y)", 
        {"i":isbn, "t":title, "a":author, "y":year})
        db.commit()

if __name__ == "__main__":
    main()