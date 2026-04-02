import time
import random

from database import SessionLocal, AnimeModel, init_db
import playwright_stealth as ps
from playwright.sync_api import sync_playwright


class ShikimoriParser:
    def __init__(self, db_session):
        self.db_session = db_session
        self.animes = {}
        # self.output_path = "anime_data.csv"

    def save_to_db(self, data):
        new_anime = AnimeModel(
            title=data.get("Название"),
            anime_type=data.get("Тип"),
            episodes=data.get("Эпизоды"),
            rating=data.get("Рейтинг"),
            score=data.get("Оценка")
        )
        self.db_session.add(new_anime)
        self.db_session.commit()

    def get_text(self, selector: str):
        try:
            element = self.page.locator(selector)
            return element.inner_text(timeout=3000).strip()
        except:
            return "Не указано"

    def parse(self, link: str):
        with ps.Stealth().use_sync(sync_playwright()) as p:
            browser = p.chromium.launch(headless=False, args=[
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',
            '--disable-dev-shm-usage'
        ])
            self.context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                )
            self.page = self.context.new_page()
            self.page.goto(link, wait_until="domcontentloaded")

            self.page.wait_for_selector("h1", timeout=5000)

            lines = self.page.query_selector_all(".line")
            
            anime_info = {"Название": "Не указано",
                        "Тип": "Не указано",
                        "Эпизоды": "Не указано",
                        "Рейтинг": "Не указано",
                        "Оценка": "Не указано"}

            anime_info["Название"] = self.page.locator("h1").inner_text().strip()
            
            for line in lines:
                key_el = line.query_selector(".key")
                value_el = line.query_selector(".value")
                if key_el and value_el:
                    key = key_el.inner_text().strip().replace(":", "")
                    value = value_el.inner_text().strip()
                    if key in ["Тип", "Эпизоды", "Рейтинг"]:
                        anime_info[key] = value

            if anime_info["Эпизоды"] == "Не указано":
                anime_info["Эпизоды"] = "1"

            anime_info["Оценка"] = self.get_text(".score-value")

            self.save_to_db(anime_info)