import requests  # type: ignore
from bs4 import BeautifulSoup


def extract_news(parser):
    """Extract news from a given web page"""
    news_list = []

    tbl = parser.table.findAll("table")[1]
    news = tbl.findAll("tr")
    ninf = {"title": "None", "url": "None", "author": "None", "points": 0}
    for i in range(len(news) - 1):  #
        n = news[i]
        if i % 3 == 0:
            ninf = {
                "title": "None",
                "url": "None",
                "author": "None",
                "points": 0,
                "comments": 0,
            }
        if n.attrs:
            if n.attrs["class"][0] == "athing":
                ninf["title"] = n.find("span", class_="titleline").find("a").string
                link = n.find("span", class_="titleline").find("a").get("href")
                if "http" in link:
                    ninf["url"] = link
                elif "item" in link:
                    ninf["url"] = "https://news.ycombinator.com/" + link
        else:
            if n.find("span", class_="subline"):
                ninf["points"] = int(n.find("span", class_="subline").find("span", class_="score").string.split()[0])
                ninf["author"] = n.find("span", class_="subline").find("a", class_="hnuser").string
                com = str(n.find("span", class_="subline").findAll("a")[-1].string.split()[0])
                if com.isdigit():
                    ninf["comments"] = int(com)
                else:
                    ninf["comments"] = 0
            news_list.append(ninf)
    return news_list


def extract_next_page(parser):
    """Extract next page URL"""
    return parser.table.findAll("table")[1].findAll("tr")[-1].contents[2].find("a").get("href")


def get_news(url, n_pages=1):
    """Collect news from a given web page"""
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news


if __name__ == "__main__":
    url = "https://news.ycombinator.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    news_list = get_news(url, n_pages=1)
    for l in news_list:
        print(l)
    with open("my.html", "w") as f:
        f.write(soup.prettify())
