from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from helper.WindowHelper import WindowHelper
from pages import HometaxInquireDataPage


class HometaxInputOfficePage:
    WINDOW_TITLE = '근무처조회/입력'
    INPUT_CORPORATE_NUMBER = (By.ID, 'gridNowWa_cell_0_1_text')
    CONFIRM_BUTTON = (By.XPATH, '//*[@id="gridNowWa_cell_0_2"]/button')
    INPUT_TOTAL_INCOME = (By.ID, 'gridNowWa_cell_0_4_text')
    APPLY_BUTTON = (By.ID, 'trigger17')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def input_corporate_number(self, corporate_registration_number):
        input_element = self.wait.until(ec.visibility_of_element_located(self.INPUT_CORPORATE_NUMBER))
        input_element.send_keys(corporate_registration_number)

    def click_confirm_button(self):
        self.driver.find_element(*self.CONFIRM_BUTTON).click()

    def input_total_income(self, total_income):
        self.driver.find_element(*self.INPUT_TOTAL_INCOME).send_keys(total_income)

    def click_apply_button(self):
        self.driver.find_element(*self.APPLY_BUTTON).click()
        self.wait.until(ec.alert_is_present())
        self.driver.switch_to.alert.accept()
        self.wait.until(ec.number_of_windows_to_be(1))
        WindowHelper(self.driver).switch_to_window_by_title(HometaxInquireDataPage.HometaxInquireDataPage.WINDOW_TITLE)
        return HometaxInquireDataPage.HometaxInquireDataPage(self.driver)
