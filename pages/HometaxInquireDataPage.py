from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class HometaxInquireDataPage:
    WINDOW_TITLE = '국세청 홈택스 - 연말정산간소화 > 근로자 > 소득ㆍ세액공제 자료 조회/발급'
    MODAL_POPUP = (By.ID, 'uteyscaa80popup')
    MODAL_FRAME = (By.ID, 'uteyscaa80popup_iframe')
    BUTTON_CLOSE_MODAL = (By.ID, 'trigger2')
    FRAME = (By.ID, 'txppIframe')
    DATA_ELEMENTS = (By.CSS_SELECTOR, '#ddcCulsUl li a')
    BUTTON_OPEN_WRITE_NEW_DEDUCTION_FORM_MODAL = (By.ID, 'btnYrsSrvc01_TODO')
    FRAME_WRITE_NEW_DEDUCTION_FORM_MODAL = (By.ID, 'ysCmShowMultiElecDcmDwld_iframe')
    BUTTON_WRITE_NEW_DEDUCTION_FORM = (By.ID, 'btnYrsSrvc01')
    MODAL_WRITE_NEW_DEDUCTION_FORM = (By.ID, 'ysCmShowMultiElecDcmDwld_iframe')
    LOADING_IMAGE = (By.ID, '___processbar2_i')
    BUTTON_EDIT_DEDUCTION_FORM = (By.ID, 'trigger32')

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

    def click_write_new_deduction_form_button(self):
        self.driver.find_element(*self.BUTTON_OPEN_WRITE_NEW_DEDUCTION_FORM_MODAL).click()
        self.wait.until(ec.frame_to_be_available_and_switch_to_it(self.FRAME_WRITE_NEW_DEDUCTION_FORM_MODAL))
        self.wait_until_loading_image_disappear()
        write_new_button = self.wait.until(ec.element_to_be_clickable(self.BUTTON_WRITE_NEW_DEDUCTION_FORM))
        write_new_button.click()
        self.check_presence_of_written_form()  # 이미 작성된 공제신고서가 있는 경우, 알림 창이 나타남

    def wait_until_loading_image_disappear(self):
        self.wait.until(ec.presence_of_element_located(self.LOADING_IMAGE))
        self.wait.until(ec.invisibility_of_element(self.LOADING_IMAGE))

    def check_presence_of_written_form(self):
        try:
            self.wait.until(ec.alert_is_present())
            self.driver.switch_to.alert.accept()
        except TimeoutException:
            print('No alert is present')

    def click_edit_deduction_form_button(self):
        self.wait.until(ec.frame_to_be_available_and_switch_to_it(self.FRAME))
        edit_deduction_form_button = self.wait.until(ec.element_to_be_clickable(self.BUTTON_EDIT_DEDUCTION_FORM))
        edit_deduction_form_button.click()

