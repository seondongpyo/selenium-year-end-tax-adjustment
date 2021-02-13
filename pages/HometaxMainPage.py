from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from pages.HometaxYearEndTaxAdjustmentPage import HometaxYearEndTaxAdjustmentPage


class HometaxMainPage:
    BUTTON_NAVIGATE_TO_SIMPLIFIED_PAGE = (By.ID, 'menuAtag_0112100000')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate_to_simplified_page(self):
        button = self.wait.until(ec.presence_of_element_located(self.BUTTON_NAVIGATE_TO_SIMPLIFIED_PAGE))
        self.driver.execute_script('arguments[0].click()', button)
        self.wait.until(ec.title_is('국세청 홈택스 - 연말정산간소화'))
        return HometaxYearEndTaxAdjustmentPage(self.driver)
