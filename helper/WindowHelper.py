from selenium.webdriver.support.wait import WebDriverWait


class WindowHelper:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def switch_to_window_by_title(self, window_title):
        current_windows = self.driver.window_handles
        for current_window in current_windows:
            self.driver.switch_to.window(current_window)
            if self.driver.title == window_title:
                break
