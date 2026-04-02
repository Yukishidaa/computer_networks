import time
import random
import csv
import os

import playwright_stealth as ps
from playwright.sync_api import sync_playwright


class ShikimoriParser:
    def __init__(self):
        self.animes = {}
        self.output_path = "anime_data.csv"

    def save_to_csv(self, data_dict):
        file_exists = os.path.isfile(self.output_path)
        with open(self.output_path, mode='a', encoding='utf-8', newline='') as f:
            fieldnames = data_dict.keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(data_dict)

    def get_text(self, selector: str):
        try:
            element = self.page.locator(selector)
            return element.inner_text(timeout=3000).strip()
        except:
            return "Не указано"
    
    def parse_page(self, link: str):
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

        self.save_to_csv(anime_info)

    def parse(self):
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
            for num_page in range(1, 10):
                self.page.goto(f"https://shikimori.one/animes?page={num_page}")
                time.sleep(random.uniform(2, 5))
                anime_links = []
                for anime in self.page.query_selector_all(".cover"):
                    link = anime.get_attribute("href")
                    if link:
                        anime_links.append(link)

                for link in anime_links:
                    self.parse_page(link)

if __name__ == "__main__":
    ShikimoriParser().parse()