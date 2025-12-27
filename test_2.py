# Проверка преобразования единиц измерения
import os
from playwright.sync_api import sync_playwright, Route
from generate_response import generate_response


def test_2():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        replaceable_responses = [
            generate_response(co2=1, energy=50, water=999),  # ОР: co2 = 1 кг, energy = 50 кВт/ч, water = 999 л
            generate_response(co2=1000, energy=1000, water=1000),  # ОР: co2 = 1 т, energy = 1 МВт/ч, water = 1 м3
            generate_response(co2=1000000, energy=1000000, water=1000000),  # ОР: co2 = 1 тыс. т, energy = 1 тыс. МВт/ч, water = 1 тыс. м3
            generate_response(co2=1000000000, energy=1000000000, water=1000000000),  # ОР: co2 = 1 млн. т, energy = 1 млн. МВт/ч, water = 1 млн. м3
            generate_response(co2=1000000000000, energy=1000000000000, water=1000000000000),  # ОР: co2 = 1 млрд. т, energy = 1 млрд. МВт/ч, water = 1 млрд. м3
            generate_response(co2=1000000000000000, energy=1000000000000000, water=1000000000000000)  # ОР: co2 = 1 квдрлн. т, energy = 1 квдрлн. МВт/ч, water = 1 квдрлн. м3
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

            screenshot_path = {"path": os.path.join("output", f"test_2_{index+1}.png")}
            load_counter.screenshot(**screenshot_path)

        context.close()
        browser.close()
