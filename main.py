from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import *

from util.selenium_process_manager import kill_selenium_chrome_driver
from pages.HometaxMainPage import HometaxMainPage

with open('private_data.txt', 'r') as file:
    lines = file.readlines()

certificate_password = lines[0].replace('\n', '')
corporate_registration_number = lines[1].replace('\n', '')
total_income = lines[2].replace('\n', '')

driver = webdriver.Chrome(ChromeDriverManager().install())  # 셀레늄 드라이버 초기화
wait = WebDriverWait(driver, 5)  # 명시적 대기를 위한 WebDriverWait 생성

# 홈택스 메인 페이지로 이동
hometax_url = 'https://hometax.go.kr/websquare/websquare.html?w2xPath=/ui/pp/index.xml'
driver.get(hometax_url)

# 연말정산간소화 페이지로 이동
main_page = HometaxMainPage(driver)
simplified_page = main_page.navigate_to_simplified_page()
simplified_page.navigate_to_login_by_certificate_page()
simplified_page.wait_until_loading_image_disappear()

simplified_page.click_login_by_certificate_button()  # 공동인증서 로그인 버튼 클릭 클릭
simplified_page.input_certificate_password(certificate_password)  # 공동인증서 비밀번호 입력
simplified_page.click_confirm_button()  # 확인 버튼 클릭

# 공동인증서 로그인 이후 '연말정산간소화 자료 조회'에서 '조회' 버튼 클릭
inquire_data_page = simplified_page.click_inquire_data_button()

inquire_data_page.close_notice_modal()  # 유의사항 안내 모달 닫기
inquire_data_page.inquire_data_by_month()  # 소득 및 세액공제 자료 조회
inquire_data_page.click_write_new_deduction_form_button()  # '공제신고서 작성' 버튼 클릭
inquire_data_page.click_edit_deduction_form_button()  # 공제신고서 수정하기 버튼 클릭

# Step.01 기본사항 입력 탭 클릭
input_basic_data_tab = wait.until(ec.element_to_be_clickable((By.ID, 'tabControl1_tab_tabs2')))
input_basic_data_tab.click()
wait.until(ec.number_of_windows_to_be(2))

# 근무처조회/입력 팝업 창으로 이동
current_windows = driver.window_handles
for current_window in current_windows:
    driver.switch_to.window(current_window)
    if '근무처조회/입력' == driver.title:
        break

# 근무처 사업자번호 입력
input_corporate_number = wait.until(ec.visibility_of_element_located((By.ID, 'gridNowWa_cell_0_1_text')))
input_corporate_number.send_keys(corporate_registration_number)
driver.find_element_by_xpath('//*[@id="gridNowWa_cell_0_2"]/button').click()

# 총급여 입력
driver.find_element_by_id('gridNowWa_cell_0_4_text').send_keys(total_income)

# 반영하기 버튼 클릭
driver.find_element_by_id('trigger17').click()
wait.until(ec.alert_is_present())
driver.switch_to.alert.accept()

# 저장 후 다음이동 버튼 클릭
wait.until(ec.number_of_windows_to_be(1))
current_windows = driver.window_handles
for current_window in current_windows:
    driver.switch_to.window(current_window)
    if '국세청 홈택스 - 연말정산간소화 > 근로자 > 소득ㆍ세액공제 자료 조회/발급' == driver.title:
        break

driver.switch_to.frame('txppIframe')
driver.find_element_by_id('trigger25').click()
wait.until(ec.alert_is_present())
driver.switch_to.alert.accept()

# '부양가족 입력'에서 저장 후 다음이동 버튼 클릭
wait.until(ec.visibility_of_element_located((By.ID, 'textbox1034')))
driver.find_element_by_id('btnSaveNext').click()
wait.until(ec.alert_is_present())
driver.switch_to.alert.accept()

# '공제항목별 지출명세 작성'에서 다음이동 버튼 클릭
wait.until(ec.visibility_of_element_located((By.ID, 'textbox1033')))
driver.find_element_by_id('textbox1367').click()
wait.until(ec.alert_is_present())
driver.switch_to.alert.accept()

# '공제신고서 내용 확인'에서 공제신고서 PDF다운로드 버튼 클릭
wait.until(ec.visibility_of_element_located((By.ID, 'trigger41')))
driver.find_element_by_id('trigger41').click()

# chromedriver.exe 종료
kill_selenium_chrome_driver()