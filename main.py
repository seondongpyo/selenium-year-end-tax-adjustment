from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

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
    login_by_certificate_button = wait.until(ec.element_to_be_clickable((By.ID, 'group91882124')))
    login_by_certificate_button.click()

    # chromedriver.exe 종료
    kill_selenium_chrome_driver()

except Exception as e:
    print('예외 발생', e)
