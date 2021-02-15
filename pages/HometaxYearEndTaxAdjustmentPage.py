from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from pages.HometaxInquireDataPage import HometaxInquireDataPage


class HometaxYearEndTaxAdjustmentPage:
    WINDOW_TITLE = '국세청 홈택스 - 연말정산간소화'
    FRAME = (By.ID, 'txppIframe')
    BUTTON_NAVIGATE_TO_LOGIN_BY_CERTIFICATE_PAGE = (By.ID, 'textbox103999')
    LOADING_IMAGE = (By.ID, '___processbar2_i')
    BUTTON_LOGIN_BY_CERTIFICATE = (By.ID, 'group91882124')
    FRAME_CERTIFICATE = (By.ID, 'dscert')
    MODAL_CERTIFICATE = (By.ID, 'ML_window')
    LOADING_CERTIFICATE = (By.XPATH, '/html/body/div[13]')
    INPUT_CERTIFICATE_PASSWORD = (By.ID, 'input_cert_pw')
    BUTTON_CONFIRM = (By.ID, 'btn_confirm_iframe')
    BUTTON_INQUIRE_DATA = (By.ID, 'textbox10400')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate_to_login_by_certificate_page(self):
        self.wait.until(ec.frame_to_be_available_and_switch_to_it(self.FRAME))
        button = self.wait.until(ec.element_to_be_clickable(self.BUTTON_NAVIGATE_TO_LOGIN_BY_CERTIFICATE_PAGE))
        button.click()

    def click_login_by_certificate_button(self):
        login_button = self.wait.until(ec.element_to_be_clickable(self.BUTTON_LOGIN_BY_CERTIFICATE))
        login_button.click()
        self.wait.until(ec.frame_to_be_available_and_switch_to_it(self.FRAME_CERTIFICATE))
        self.wait.until(ec.visibility_of_element_located(self.MODAL_CERTIFICATE))  # 공인인증서 창이 나타날 때까지 대기
        self.wait.until(ec.invisibility_of_element(self.LOADING_CERTIFICATE))  # 로딩 이미지가 사라질 때까지 대기

    def input_certificate_password(self, certificate_password):
        input_password = self.wait.until(ec.element_to_be_clickable(self.INPUT_CERTIFICATE_PASSWORD))
        input_password.send_keys(certificate_password)  # 공인인증서 비밀번호 입력

    def click_confirm_button(self):
        self.driver.find_element(*self.BUTTON_CONFIRM).click()  # 확인 버튼 클릭

    def click_inquire_data_button(self):
        self.wait.until(ec.frame_to_be_available_and_switch_to_it(self.FRAME))
        inquiry_button = self.wait.until(ec.presence_of_element_located(self.BUTTON_INQUIRE_DATA))
        inquiry_button.click()
        return HometaxInquireDataPage(self.driver)

    def wait_until_loading_image_disappear(self):
        self.wait.until(ec.presence_of_element_located(self.LOADING_IMAGE))
        self.wait.until(ec.invisibility_of_element(self.LOADING_IMAGE))
