import allure
from pages.page_authorization import FormPageAuthorization
from configuration import SERVICE_URL
from enums.global_exception import GlobalErrorMessages


class TestFormPage:

    def test_authorization(self, driver):
        form_page = FormPageAuthorization(driver, SERVICE_URL)
        form_page.open()
        form_page.fill_fields_authorization()
        result = form_page.result_authorization()
        assert result == 'Личный кабинет', GlobalErrorMessages.WRONG_STATUS
