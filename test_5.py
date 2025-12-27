# Проверка адаптива отображения счётчиков в меньшем разрешении
import os
from playwright.sync_api import sync_playwright


def test_5():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.set_viewport_size({"width": 1024, "height": 768})
        page.goto("https://www.avito.ru/avito-care/eco-impact")

        load_counter = page.locator(".desktop-wrapper-OutiE")
        load_counter.wait_for()

        screenshot_path = {"path": os.path.join("output", "test_5.png")}
        load_counter.screenshot(**screenshot_path)

        context.close()
        browser.close()
