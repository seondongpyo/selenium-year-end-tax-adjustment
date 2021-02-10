from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import *

from util.selenium_process_manager import kill_selenium_chrome_driver

try:
    driver = webdriver.Chrome(ChromeDriverManager().install())  # 셀레늄 드라이버 초기화
    wait = WebDriverWait(driver, 5)  # 명시적 대기를 위한 WebDriverWait 생성

    # 홈택스 메인 페이지로 이동
    hometax_url = 'https://hometax.go.kr/websquare/websquare.html?w2xPath=/ui/pp/index.xml'
    driver.get(hometax_url)

    # 연말정산간소화 페이지로 이동
    navigate_to_simplified_page = wait.until(ec.presence_of_element_located((By.ID, 'menuAtag_0112100000')))
    driver.execute_script('arguments[0].click()', navigate_to_simplified_page)
    wait.until(ec.title_is('국세청 홈택스 - 연말정산간소화'))

    # 공동인증서 로그인 클릭
    wait.until(ec.frame_to_be_available_and_switch_to_it((By.ID, 'txppIframe')))
    login_button = wait.until(ec.element_to_be_clickable((By.ID, 'textbox103999')))
    login_button.click()
    
    # 로딩 대기
    wait.until(ec.presence_of_element_located((By.ID, '___processbar2_i')))
    wait.until(ec.invisibility_of_element((By.ID, '___processbar2_i')))
    
    # 공동인증서 로그인 버튼 클릭
    login_by_certificate_button = wait.until(ec.element_to_be_clickable((By.ID, 'group91882124')))
    login_by_certificate_button.click()

    # 공동인증서가 하나일 경우...
    wait.until(ec.frame_to_be_available_and_switch_to_it((By.ID, 'dscert')))
    wait.until(ec.visibility_of_element_located((By.ID, 'ML_window')))  # 공인인증서 창이 나타날 때까지 대기
    wait.until(ec.invisibility_of_element((By.XPATH, '/html/body/div[13]')))  # 로딩 이미지가 사라질 때까지 대기
    input_password = wait.until(ec.element_to_be_clickable((By.ID, 'input_cert_pw')))
    certificate_password = open('private_data.txt', 'r').readline()
    input_password.send_keys(certificate_password)  # 공인인증서 비밀번호 입력
    driver.find_element_by_id('btn_confirm_iframe').click()  # 확인 버튼 클릭

    # 공동인증서 로그인 이후 '연말정산간소화 자료 조회'에서 '조회' 버튼 클릭
    wait.until(ec.frame_to_be_available_and_switch_to_it((By.ID, 'txppIframe')))
    search_button = wait.until(ec.presence_of_element_located((By.ID, 'textbox10400')))
    search_button.click()

    # 유의사항 안내 모달 닫기
    wait.until(ec.visibility_of_element_located((By.ID, 'uteyscaa80popup')))
    wait.until(ec.frame_to_be_available_and_switch_to_it((By.ID, 'uteyscaa80popup_iframe')))
    close_button = wait.until(ec.visibility_of_element_located((By.ID, 'trigger2')))
    close_button.click()

    # 소득 및 세액공제 자료 조회
    wait.until(ec.frame_to_be_available_and_switch_to_it((By.ID, 'txppIframe')))
    link_elements = wait.until(ec.visibility_of_all_elements_located((By.CSS_SELECTOR, '#ddcCulsUl li a')))
    for link_element in link_elements:
        link_element.click()

    # '공제신고서 작성' 버튼 클릭
    driver.find_element_by_id('btnYrsSrvc01_TODO').click()
    wait.until(ec.frame_to_be_available_and_switch_to_it((By.ID, 'ysCmShowMultiElecDcmDwld_iframe')))
    wait.until(ec.presence_of_element_located((By.ID, '___processbar2_i')))
    wait.until(ec.invisibility_of_element((By.ID, '___processbar2_i')))
    write_new_button = wait.until(ec.element_to_be_clickable((By.ID, 'btnYrsSrvc01')))
    write_new_button.click()

    # 이미 작성된 공제신고서가 있는 경우, 알림 창이 나타남
    try:
        wait.until(ec.alert_is_present())
        driver.switch_to.alert.accept()
    except TimeoutException:
        print('No alert is present')

    # 공제신고서 수정하기 버튼 클릭
    wait.until(ec.title_is('국세청 홈택스 - 연말정산간소화 > 근로자 > 소득ㆍ세액공제 자료 조회/발급'))
    wait.until(ec.frame_to_be_available_and_switch_to_it((By.ID, 'txppIframe')))
    edit_deduction_form_button = wait.until(ec.element_to_be_clickable((By.ID, 'trigger32')))
    edit_deduction_form_button.click()

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
    input_corporate_number.send_keys('1234567890')
    driver.find_element_by_xpath('//*[@id="gridNowWa_cell_0_2"]/button').click()

    # chromedriver.exe 종료
    kill_selenium_chrome_driver()

except Exception as e:
    print('예외 발생', e)
