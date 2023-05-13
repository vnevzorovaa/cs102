from sqlalchemy import Column, String, Integer  # сохранение данных в sqlite
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scraputils import get_news

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


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    url = "https://news.ycombinator.com/"
    news_list = get_news(url, n_pages=34)
    create_db(news_list)