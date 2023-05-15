import sqlalchemy
from bayes import NaiveBayesClassifier, label_news
from bottle import redirect, request, route, run, template
from db import News, session
from scraputils import get_news


@route("/all")
def all_news():
    s = session()
    rows = s.query(News).all()
    return template("news_template2", rows=rows)


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/", method="GET")
def add_label():
    s = session()
    label = request.GET.get("label", "")
    id = int(request.GET.get("id", ""))
    row = s.query(News).filter(News.id == id).one()
    row.label = label
    s.add(row)
    s.commit()
    redirect("/all")
    return row


@route("/update")
def update_news():
    s = session()
    url = "https://news.ycombinator.com/"
    lst = get_news(url)
    for dic in lst:
        try:
            row = s.query(News).filter(News.title == dic["title"]).one()
        except sqlalchemy.exc.NoResultFound:
            new = News(
                title=dic["title"],
                author=dic["author"],
                url=dic["url"],
                comments=dic["comments"],
                points=dic["points"],
            )
            s.add(new)
            s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    label_news()
    redirect("/news")


if __name__ == "__main__":
    run(host="localhost", port=8080)
