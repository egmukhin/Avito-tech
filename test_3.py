# Проверка округления счётчиков
import os
from playwright.sync_api import sync_playwright, Route
from generate_response import generate_response


def test_3():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        replaceable_responses = [
            generate_response(co2=0.3, energy=0.5, water=0.9),
            generate_response(co2=1050, energy=1150, water=1250),
            generate_response(co2=1450, energy=1550, water=1350),
            generate_response(co2=1850, energy=1750, water=1650),
            generate_response(co2=9990, energy=9949, water=9950)
        ]

        for index, value in enumerate(replaceable_responses):
            def change_response(route: Route):
                route.fulfill(
                    body=value
                )

            page.route("**/web/1/charity/ecoImpact/init", change_response)
            page.goto("https://www.avito.ru/avito-care/eco-impact")

            load_counter = page.locator(".desktop-impact-items-F7T6E")
            load_counter.wait_for()

            screenshot_path = {"path": os.path.join("output", f"test_3_{index+1}.png")}
            load_counter.screenshot(**screenshot_path)

        context.close()
        browser.close()
