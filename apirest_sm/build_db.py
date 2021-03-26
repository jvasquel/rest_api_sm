"""
This program builds the author_book_publisher Sqlite database from the
author_book_publisher.csv file.
"""
from datetime import datetime
import os
import csv
from importlib import resources
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/home/jose/Desktop/project/modules')
sys.path.insert(2, '/home/jose/Desktop/project/data/author_book_publisher.csv')
sys.path.insert(3, '/home/jose/Desktop/project/data/author_book_publisher.db')
print ('path')
print (sys.path[2])
import states

from states import Parameter, UserModel, Device, State



def get_author_book_publisher_data():
    """
    This function gets the data from the csv file
    """
    with open(sys.path[2]) as csvfile:
        csv_reader = csv.DictReader(csvfile)
        data = [row for row in csv_reader]
        return data

def get_driver(session):
    
    author_name=input('inserta el nombre del driver: '),
    book_title=input('inserta el rut del diver: '),
    
    
def populate_database(session, author_book_publisher_data):
    # insert the data
    for row in author_book_publisher_data:

        author = (
            session.query(Author)
            .filter(Author.last_name == row["last_name"])
            .one_or_none()
        )
        if author is None:
            author = Author(
                first_name=row["first_name"], last_name=row["last_name"]
            )
            session.add(author)

        book = (
            session.query(Book)
            .filter(Book.title == row["title"])
            .one_or_none()
        )
        if book is None:
            book = Book(title=row["title"],date=datetime.now())
            session.add(book)
       

        publisher = (
            session.query(Publisher)
            .filter(Publisher.name == row["publisher"])
            .one_or_none()
        )
        if publisher is None:
            publisher = Publisher(name=row["publisher"])
            session.add(publisher)

        # add the items to the relationships
        author.books.append(book)
        author.publishers.append(publisher)
        publisher.authors.append(author)
        publisher.books.append(book)
        session.commit()

    session.close()


def main():
    print("starting")
  
        # does the database exist?
    if os.path.exists('/database.db'):
        os.remove('/database.db')

    # create the database
    engine = create_engine(f"sqlite:///database.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    #populate_database(session, author_book_publisher_data)

    print("finished")


if __name__ == "__main__":
    main()
