# Проверка на отображение невалидных данных
import os
from playwright.sync_api import sync_playwright, Route
from generate_response import generate_response


def test_4():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        replaceable_responses = [
            generate_response(co2=None, energy="string", water=-99),
            generate_response(co2=True, energy=False, water=[-3]),
            generate_response(co2=[5, 2], energy={}, water="")
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

            screenshot_path = {"path": os.path.join("output", f"test_4_{index+1}.png")}
            load_counter.screenshot(**screenshot_path)

        context.close()
        browser.close()
