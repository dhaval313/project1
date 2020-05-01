import requests
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine=create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    li=db.execute("select isbn from books").fetchone()
    for isbn in li:
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "OT2oBaEabBiJLpfBNPeEqA", "isbns": li})
        if res.status_code != 200:
            raise Exception("error: wrong line of code")
        data = res.json()
        db.execute("insert into ratings (isbn, count, avg_ratings) values (:isbn, :count, :avg_ratings)",
                    {"isbn": data["books"]["isbn"],"count": data["books"]["work_ratings_count"], "avg_ratings": data["books"]["average_rating"]})
        print(f"added {isbn}")
    db.commit()

if __name__=="__main__":
    main()