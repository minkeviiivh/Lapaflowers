from pages.page_parameter_selection import FormPageParametrSelection
from configuration import SERVICE_URL
from enums.global_exception import GlobalErrorMessages
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import allure



@allure.suite('Elements #7')
@allure.feature('Parameter Selection')
class TestFormPage:

    @allure.title('Check Parametr Selection')
    def test_parameter_selection(self, driver):
        with allure.step('Go to page'):
            form_page = FormPageParametrSelection(driver, SERVICE_URL)
            form_page.open()
        with allure.step('Go to catalog'):
            form_page.fields_catalog_flowers()
            form_page.catalog_flowers_all()
            form_page.parameter_selection()
        with allure.step('Gathering information from the page'):
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
        with allure.step('Checking Values'):
            for price in prices:
                result = re.match(r'(\w+)', price)
                assert 60 <= int(result.group(0)) <= 130, GlobalErrorMessages.WRONG_STATUS





