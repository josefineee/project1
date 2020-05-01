import os
import csv

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
db = scoped_session(sessionmaker(bind=engine)) 

def main():
    fil = open("books.csv")
    read = csv.reader(fil)
    next(read, None)
    for isbn, title, author, year in read: 
        year = int(year)
        db.execute("INSERT INTO books(isbn, title, author, year) VALUES (:i, :t, :a, :y)", 
        {"i":isbn, "t":title, "a":author, "y":year})
    db.commit()

if __name__ == "__main__":
    if not engine.dialect.has_table(db,"books"): 
        db.execute("CREATE TABLE books (id SERIAL PRIMARY KEY, isbn VARCHAR NOT NULL, title VARCHAR NOT NULL, author VARCHAR NOT NULL, year INTEGER NOT NULL)")
        db.commit()
    main()