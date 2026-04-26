import os
import re
import json
import hashlib
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any

import feedparser
import requests
from dateutil import parser as dateparser
import pytz
from jinja2 import Environment, FileSystemLoader
from tenacity import retry, stop_after_attempt, wait_exponential

# ---------------- CONFIG ---------------- #

FEEDS = [
    "https://www.geeky-gadgets.com/feed/",
    "https://www.google.com/alerts/feeds/03013219760151597796/2175154584174914156",
    "https://www.geeky-gadgets.com/feed/",
    "https://feed.infoq.com/",
    "https://www.opensourceprojects.dev/rss",
    "https://www.scmp.com/rss/36/feed/",
    "https://techcrunch.com/feed/",
    "https://www.google.ru/alerts/feeds/03013219760151597796/5728673472518424448",
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.wundertech.net/feed/",
    "https://www.digitalocean.com/blog/feed",
    "https://www.servethehome.com/feed/",
    "https://www.reddit.com/r/selfhosted/.rss",
    "https://www.reddit.com/r/rss/.rss",
    "https://www.reddit.com/r/homelab/.rss",
    "https://hnrss.org/frontpage",
    "https://www.phoronix.com/rss.php",
    "https://lwn.net/headlines/rss",
    "https://planet.debian.org/rss20.xml",
    "https://archlinux.org/feeds/news/",
    "https://itsfoss.com/feed/",
    "https://www.omgubuntu.co.uk/feed",
    "https://www.zdnet.com/topic/security/rss.xml",
    "https://krebsonsecurity.com/feed/",
    "https://www.bleepingcomputer.com/feed/",
    "https://www.darkreading.com/rss.xml",
    "https://www.csoonline.com/feed",
    "https://www.schneier.com/blog/atom.xml",
    "https://feeds.arstechnica.com/arstechnica/index",
    "https://www.theverge.com/rss/index.xml",
    "https://www.engadget.com/rss.xml",
    "https://www.wired.com/feed/rss",
    "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "https://www.ft.com/technology?format=rss",
    "https://www.economist.com/science-and-technology/rss.xml",
    "https://spectrum.ieee.org/rss/fulltext",
    "https://towardsdatascience.com/feed",
    "https://machinelearningmastery.com/blog/feed/",
    "https://openai.com/blog/rss.xml",
    "https://deepmind.google/blog/rss.xml",
    "https://ai.googleblog.com/feeds/posts/default",
    "https://www.marktechpost.com/feed/",
    "https://venturebeat.com/category/ai/feed/",
    "https://syncedreview.com/feed/",
    "https://www.unite.ai/feed/",
    "https://www.artificialintelligence-news.com/feed/"
]

TOPIC_KEYWORDS = {
    "AI": ["ai", "machine learning", "llm", "gpt", "deep learning"],
    "Robot": ["robot", "robotics", "autonomous", "automation", "humanoid", "drone"],
    "Chip": ["chip", "chips", "semiconductor", "silicon", "wafer"],
    "Cybersecurity": ["security", "hack", "malware", "vulnerability"],
    "Hardware": ["chip", "semiconductor", "gpu", "nvidia"],
    "Science": ["research", "paper", "discovery"],
    "Creative": ["music", "art", "generative", "creative"]
}

TIMEZONE = pytz.timezone("Asia/Ho_Chi_Minh")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (NewsAggregatorBot/1.0)"
}

MAX_DAILY_ARTICLES = 1000

logging.basicConfig(level=logging.INFO)

# ---------------- HELPERS ---------------- #

def today_date():
    return datetime.now(TIMEZONE).date()

def clean_html(raw):
    return re.sub('<.*?>', '', raw or '')

def extract_domain(url):
    return re.findall(r'https?://([^/]+)/?', url)[0]

def hash_id(text):
    return hashlib.md5(text.encode()).hexdigest()

def match_topics(text: str) -> List[str]:
    text = text.lower()
    matched = []
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(k in text for k in keywords):
            matched.append(topic)
    return matched

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def fetch_feed(url):
    return feedparser.parse(url)

def parse_entry(entry, source):
    title = entry.get("title", "")
    link = entry.get("link", "")
    summary = clean_html(entry.get("summary", ""))[:200]

    date = None
    for key in ["published", "updated"]:
        if entry.get(key):
            try:
                date = dateparser.parse(entry.get(key))
                break
            except:
                pass

    if not date:
        return None

    date = date.astimezone(TIMEZONE)

    if date.date() != today_date():
        return None

    topics = match_topics(title + " " + summary)
    if not topics:
        return None

    return {
        "id": hash_id(link or title),
        "title": title,
        "link": link,
        "summary": summary,
        "date": date.isoformat(),
        "source": source,
        "topics": topics
    }

def fetch_all_articles():
    articles = []

    for url in FEEDS:
        try:
            feed = fetch_feed(url)
            source = feed.feed.get("title", extract_domain(url))

            for entry in feed.entries:
                parsed = parse_entry(entry, source)
                if parsed:
                    articles.append(parsed)

        except Exception as e:
            logging.warning(f"Failed feed {url}: {e}")

    return dedupe_articles(articles)

def dedupe_articles(articles):
    seen = {}
    for a in articles:
        key = a["link"]
        if key not in seen:
            seen[key] = a
    return list(seen.values())


def limit_articles(articles):
    if len(articles) <= MAX_DAILY_ARTICLES:
        return articles

    sorted_articles = sorted(articles, key=lambda a: a["date"], reverse=True)
    logging.info(f"Trimming articles to the latest {MAX_DAILY_ARTICLES} of {len(articles)} collected today")
    return sorted_articles[:MAX_DAILY_ARTICLES]

# ---------------- OUTPUT ---------------- #

def save_markdown(articles):
    folder = f"articles/{today_date()}"
    os.makedirs(folder, exist_ok=True)

    for a in articles:
        filename = os.path.join(folder, f"{a['id']}.md")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"""---
title: "{a['title']}"
date: "{a['date']}"
source: "{a['source']}"
link: "{a['link']}"
topics: {a['topics']}
---

{a['summary']}
""")

def save_llm_txt(articles):
    with open("today_llm.txt", "w", encoding="utf-8") as f:
        for a in articles:
            f.write(f"{a['title']} - {a['link']}\n")

def generate_html(articles):
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("template.html")
    html = template.render(articles=articles)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

# ---------------- MAIN ---------------- #

def main():
    logging.info("Fetching articles...")
    articles = limit_articles(fetch_all_articles())

    logging.info(f"Collected {len(articles)} articles")

    save_markdown(articles)
    save_llm_txt(articles)
    generate_html(articles)

    logging.info("Done.")

if __name__ == "__main__":
    main()