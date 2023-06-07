from bs4 import BeautifulSoup
from urllib.parse import urlparse
from credentials import *
import math

with open("utils/blacklist.txt") as f:
    domains_blacklist = set(f.read().split("\n"))

def get_page_content(row):
    # parse html form each page
    soup = BeautifulSoup(row["html"])
    text = soup.get_text()
    return text

def tracker_urls(row):
    soup = BeautifulSoup(row["html"])
    # Find Google Analytics/managers etc. stuff
    # get all scripts from page
    scripts = soup.find_all("script", {"src": True})
    srcs = [s.get("src") for s in scripts]

    # get all links from page
    links = soup.find_all("a", {"href": True})
    href = [l.get("href") for l in links]
    # get links like this : "https://googlemanager.com/script.js"
    # and parse to this -> "googlemanager.com" [ LEAVE FOR US THE ROOT DOMAIN ]
    all_domains = [urlparse(s).hostname for s in srcs + href]
    # bad_domanis this is document from here:
    # https://raw.githubusercontent.com/notracking/hosts-blocklists/master/dnscrypt-proxy/dnscrypt-proxy.blacklist.txt

    bad_domains = [a for a in all_domains if a in domains_blacklist]
    return len(bad_domains)

def user_opinion(row):
    score = row["relevance"]

    print(type(row))

    # if(not math.isnan(score)):
    #     return score
    return 0

class Filter():
    def __init__(self,results):
        self.filtered = results.copy()

    def page_content_filter(self):
        page_content = self.filtered.apply(get_page_content, axis=1)
        # how many words in page
        word_count = page_content.apply(lambda x: len(x.split(" ")))
        # comparing amount of words between pages
        word_count /= word_count.median()
        # penalty to the rank based on if the content has enough words or not
        word_count[word_count <= .5] = RESULT_COUNT
        word_count[word_count != RESULT_COUNT] = 0
        self.filtered["rank"] += word_count

    def tracker_filter(self):
        tracker_count = self.filtered.apply(tracker_urls, axis=1)
        tracker_count[tracker_count > tracker_count.median()] = RESULT_COUNT * 2
        self.filtered["rank"] += tracker_count

    def relevance_evaluator(self):
        score_count = self.filtered.apply(user_opinion, axis=1)
        self.filtered["rank"] -= score_count

    def filter(self):
        self.page_content_filter()
        self.tracker_filter()
        self.relevance_evaluator()
        # reSort our DataFrame by rank
        self.filtered = self.filtered.sort_values("rank", ascending=True)
        self.filtered["rank"] = self.filtered["rank"].round()
        return self.filtered

"""
пояснення методу page_content_filter
Ця функція призначена для фільтрації вмісту сторінок.
Основна ідея - встановити ранг (якість) для кожної сторінки на основі кількості слів у її вмісті.

Ось кроки, які вона виконує:

Вона отримує вміст кожної сторінки і рахує кількість слів у цьому вмісті.
Потім вона нормалізує ці числа, поділивши їх на медіану (середнє значення) кількості слів у всіх сторінках.
Це допомагає порівняти кількість слів на кожній сторінці відносно середньої кількості слів у всьому наборі даних.
Потім вона застосовує штраф до рангу для сторінок, у яких кількість слів менше або дорівнює 0.5.
Це означає, що сторінки з меншою кількістю слів отримують певний низький ранг, щоб вони були менш важливими.
Всі інші сторінки, які мають достатню кількість слів, отримують ранг 0, що означає, що вони є важливими.
Нарешті, цей ранг додається до наявного рангу кожної сторінки.

Таким чином, функція встановлює ранг для сторінок, враховуючи кількість слів у їх вмісті, і
надає штраф для сторінок з меншою кількістю слів.
"""