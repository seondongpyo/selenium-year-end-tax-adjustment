from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from util.selenium_process_manager import kill_selenium_chrome_driver

try:
    driver = webdriver.Chrome(ChromeDriverManager().install())  # 셀레늄 드라이버 초기화
    wait = WebDriverWait(driver, 10)  # 명시적 대기를 위한 WebDriverWait 생성

    # 홈택스 메인 페이지로 이동
    hometax_url = 'https://hometax.go.kr/websquare/websquare.html?w2xPath=/ui/pp/index.xml'
    driver.get(hometax_url)

    # 홈택스 로그인 페이지로 이동
    wait.until(ec.presence_of_element_located((By.ID, 'group1295')))  # 페이지 로딩을 위한 대기
    wait.until(ec.presence_of_element_located((By.ID, 'wfFooter')))
    login_button = wait.until(ec.element_to_be_clickable((By.ID, 'group88615548')))  # 로그인 버튼이 보일 때까지 대기
    login_button.click()

    # 아이디, 비밀번호 입력하여 로그인 시도
    wait.until(ec.title_is('국세청 홈택스 - 로그인'))
    wait.until(ec.frame_to_be_available_and_switch_to_it((By.ID, 'txppIframe')))
    driver.find_element_by_id('iptUserId').send_keys('아이디')
    driver.find_element_by_id('iptUserPw').send_keys('비밀번호')
    driver.find_element_by_id('anchor6').click()

    # chromedriver.exe 종료
    kill_selenium_chrome_driver()

except Exception as e:
    print(e)
