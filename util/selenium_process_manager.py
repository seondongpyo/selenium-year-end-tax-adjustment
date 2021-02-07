import psutil


def kill_selenium_chrome_driver():
    for process in psutil.process_iter():
        process_name = process.name()
        process_id = process.pid

        if process_name == "chromedriver.exe":
            psutil.Process(pid=process_id).kill()

            # 부모 프로세스까지 종료하려면 주석 해제
            # parent_pid = process_id
            # parent = psutil.Process(parent_pid)
            # for child in parent.children(recursive=True):
            #     child.kill()
            # parent.kill()
