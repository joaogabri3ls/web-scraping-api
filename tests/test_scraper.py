import pytest
from app.scraping.scraper import scrape_espn_news


def test_scrape_espn_news():
    url = "https://www.espn.com.br/futebol/"
    df = scrape_espn_news(url)
    assert not df.empty, "DataFrame should not be empty"
    assert all(col in df.columns for col in ["title", "summary", "date", "link"]), "Missing columns in DataFrame"
