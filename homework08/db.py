# mypy: ignore-errors
from scraputils import get_news
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def create_db(lst):
    s = session()
    ninf = {
        "title": "None",
        "url": "None",
        "author": "None",
        "points": 0,
        "comments": 0,
    }
    for dic in lst:
        if dic != ninf:
            new = News(
                title=dic["title"],
                author=dic["author"],
                url=dic["url"],
                comments=dic["comments"],
                points=dic["points"],
            )
            s.add(new)
            s.commit()


Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)


class News(Base):  # mypy: ignore all
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    url = "https://news.ycombinator.com/"
    news_list = get_news(url, n_pages=34)
    create_db(news_list)
