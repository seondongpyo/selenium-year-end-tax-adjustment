from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class HometaxYearEndTaxAdjustmentPage:
    WINDOW_TITLE = '국세청 홈택스 - 연말정산간소화'
    FRAME = (By.ID, 'txppIframe')
    BUTTON_NAVIGATE_TO_LOGIN_BY_CERTIFICATE_PAGE = (By.ID, 'textbox103999')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate_to_login_by_certificate_page(self):
        # 공동인증서 로그인 클릭
        self.wait.until(ec.frame_to_be_available_and_switch_to_it(self.FRAME))
        button = self.wait.until(ec.element_to_be_clickable(self.BUTTON_NAVIGATE_TO_LOGIN_BY_CERTIFICATE_PAGE))
        button.click()
