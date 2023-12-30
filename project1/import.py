import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import scoped_session,sessionmaker

url = 'postgresql://postgres:admin@localhost:5432/wisdom'
engine = create_engine(url)
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    read = csv.reader(f)
    id=0
    for isbn,title,author,year in read:
        title = str(title.replace("'", ""))
        year = str(year)
        author = str(author.replace("'", ""))
        year = str(year)
        id = str(id)
        insert = "insert into books (isbn, title, author, year) values (\'{isbn}\', \'{title}\', \'{author}\', \'{year}\')".format(isbn=isbn, title=title, author=author, year=year)
        db.execute(text(insert))
        # db.execute("insert into books (id, isbn, title, author, year) values (:id, :isbn, :title, :author, :year)",
        #             {"id": id, "isbn": isbn, "title": title, "author": author, "year": year})
        id = int(id)
        id+=1
        print(f"added {id},{isbn}, {title},{author},{year}")
    db.commit()

if __name__=="__main__":
    main()