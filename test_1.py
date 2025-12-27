# Проверка отображения счётчиков у НЕавторизованного пользователя
import os
from playwright.sync_api import sync_playwright


def test_1():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.avito.ru/avito-care/eco-impact")

        load_counter = page.locator(".desktop-impact-items-F7T6E")
        load_counter.wait_for()

        screenshot_path = {"path": os.path.join("output", "test_1.png")}
        load_counter.screenshot(**screenshot_path)

        context.close()
        browser.close()
