from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *


class HometaxInquireDataPage:
    WINDOW_TITLE = '국세청 홈택스 - 연말정산간소화 > 근로자 > 소득ㆍ세액공제 자료 조회/발급'
    MODAL_POPUP = (By.ID, 'uteyscaa80popup')
    MODAL_FRAME = (By.ID, 'uteyscaa80popup_iframe')
    BUTTON_CLOSE_MODAL = (By.ID, 'trigger2')
    FRAME = (By.ID, 'txppIframe')
    DATA_ELEMENTS = (By.CSS_SELECTOR, '#ddcCulsUl li a')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def close_notice_modal(self):
        try:
            self.wait.until(ec.visibility_of_element_located(self.MODAL_POPUP))
            self.wait.until(ec.frame_to_be_available_and_switch_to_it(self.MODAL_FRAME))
            close_button = self.wait.until(ec.visibility_of_element_located(self.BUTTON_CLOSE_MODAL))
            close_button.click()
        except TimeoutException:
            print('모달 창 없음')

    def inquire_data_by_month(self):
        link_elements = self.wait.until(ec.visibility_of_all_elements_located(self.DATA_ELEMENTS))
        for link_element in link_elements:
            link_element.click()
