from pages.page_catalog_flowers import FormPageFlowers
from locators.form_page_locators import FormPageLocators as Locators
from pages.page_sorting import FormPageSorting
from configuration import SERVICE_URL
from enums.global_exception import GlobalErrorMessages
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import allure


@allure.suite('Elements #8')
@allure.feature('Sorting')
class TestFormPage:

    @allure.step('Check sorting by price')
    def test_sorting(self, driver):
        svit = []
        with allure.step('Basic methods'):
            form_page = FormPageSorting(driver, SERVICE_URL + 'catalog/bukety/')
            form_page.open()
            form_page.sorting()
        with allure.step('Gathering information from the site'):
            url = driver.current_url
            user_agent = UserAgent()
            headers = {
                'User-Agent': user_agent.random
            }
            response = requests.get(url, headers=headers)
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')
            price_elements = soup.select('.produce_el_price .new')
            prices = [price_element.text.strip() for price_element in price_elements]
            for price in prices:
                result = re.match(r'(\w+)', price)
                svit.append(int(result.group(0)))
            result_sort = form_page.check_sort(svit)
        with allure.step('Checking result'):
            assert result_sort == bool(True), GlobalErrorMessages.WRONG_STATUS

    @allure.step('Check sorting by popular')
    def test_sorting_popular(self, driver):
        with allure.step('Basic methods'):
            form_page = FormPageSorting(driver, SERVICE_URL + 'catalog/bukety/')
            form_page.open()
            form_page.sorting_popular()
        with allure.step('Checking result'):
            result = form_page.get_text(Locators.RECOMMEND)
            assert result == 'Рекомендуем', GlobalErrorMessages.WRONG_STATUS
