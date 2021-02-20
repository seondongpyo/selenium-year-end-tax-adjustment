from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from pages.HometaxMainPage import HometaxMainPage
from util.selenium_process_manager import kill_selenium_chrome_driver

with open('private_data.txt', 'r', encoding='UTF8') as file:
    lines = file.readlines()

browser_name = lines[0].replace('\n', '')
certificate_owner_name = lines[1].replace('\n', '')
certificate_password = lines[2].replace('\n', '')
corporate_registration_number = lines[3].replace('\n', '')
total_income = lines[4].replace('\n', '')

driver = None
print('browser_name :', browser_name)
if browser_name == 'chrome':
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
elif browser_name == 'edge':
    driver = webdriver.Edge(executable_path=EdgeChromiumDriverManager().install())
elif browser_name == 'firefox':
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

# 홈택스 메인 페이지로 이동
hometax_url = 'https://hometax.go.kr/websquare/websquare.html?w2xPath=/ui/pp/index.xml'
driver.get(hometax_url)

# 연말정산간소화 페이지로 이동
main_page = HometaxMainPage(driver)
simplified_page = main_page.navigate_to_simplified_page()
simplified_page.navigate_to_login_by_certificate_page()
simplified_page.wait_until_loading_image_disappear()

simplified_page.click_login_by_certificate_button()  # 공동인증서 로그인 버튼 클릭 클릭
simplified_page.select_certificate_by_owner_name(certificate_owner_name)  # 이름으로 시작하는 공동인증서 찾기
simplified_page.input_certificate_password(certificate_password)  # 공동인증서 비밀번호 입력
simplified_page.click_confirm_button()  # 확인 버튼 클릭

# 공동인증서 로그인 이후 '연말정산간소화 자료 조회'에서 '조회' 버튼 클릭
inquire_data_page = simplified_page.click_inquire_data_button()
inquire_data_page.close_notice_modal()  # 유의사항 안내 모달 닫기
inquire_data_page.inquire_data_by_month()  # 소득 및 세액공제 자료 조회
inquire_data_page.click_write_new_deduction_form_button()  # '공제신고서 작성' 버튼 클릭
inquire_data_page.click_edit_deduction_form_button()  # 공제신고서 수정하기 버튼 클릭

input_office_page = inquire_data_page.click_step_1_tab()
input_office_page.input_corporate_number(corporate_registration_number)  # 근무처 사업자번호 입력
input_office_page.click_confirm_button()
input_office_page.input_total_income(total_income)  # 총급여 입력
inquire_data_page = input_office_page.click_apply_button()  # 반영하기 버튼 클릭
inquire_data_page.click_save_and_move_to_step_2_button()  # 저장 후 다음이동 버튼 클릭
inquire_data_page.click_save_and_move_to_step_3_button()  # '부양가족 입력'에서 저장 후 다음이동 버튼 클릭
inquire_data_page.click_move_to_step_4_button()  # '공제항목별 지출명세 작성'에서 다음이동 버튼 클릭
inquire_data_page.click_download_written_deduction_form_button()  # '공제신고서 내용 확인'에서 공제신고서 PDF다운로드 버튼 클릭

# chromedriver.exe 종료
kill_selenium_chrome_driver()
