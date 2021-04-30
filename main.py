from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import random
from time import sleep
import configparser
config = configparser.ConfigParser()
config.read('.env')

username = str(config.get("config", "username"))
password = str(config.get("config", "password"))


def create_driver_session(session_id, executor_url):
    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

    # Save the original function, so we can revert our patch
    org_command_execute = RemoteWebDriver.execute

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)

    # Patch the function before creating the driver object
    RemoteWebDriver.execute = new_command_execute

    new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    # Replace the patched function with original function
    RemoteWebDriver.execute = org_command_execute

    return new_driver

driver = webdriver.Chrome('./chromedriver')
executor_url = driver.command_executor._url
session_id = driver.session_id



def login(driver):
    driver.get("https://bumble.com/app")
    driver.find_element_by_xpath("/html/body/div/div/div[1]/div[2]/main/div/div[3]/form/div[1]/div/div[2]/div").click()
    driver.switch_to_window(driver.window_handles[1]) #switches to login
    driver.find_element_by_id('email').send_keys(username)
    driver.find_element_by_id('pass').send_keys(password)
    driver.find_element_by_id('pass').send_keys(Keys.ENTER)
    driver.switch_to_window(driver.window_handles[0])



def basic_like(driver):
    a = ActionChains(driver)
    a.send_keys(Keys.ARROW_RIGHT).perform()

def basic_pass(driver):
    a = ActionChains(driver)
    a.send_keys(Keys.ARROW_LEFT).perform()

def Like(driver):
    a = ActionChains(driver)
    for i in range(random.randrange(5)):
        a.send_keys(Keys.ARROW_DOWN).perform()

    a.send_keys(Keys.ARROW_RIGHT).perform()

def Pass(driver):
    a = ActionChains(driver)
    for i in range(random.randrange(5)):
        a.send_keys(Keys.ARROW_DOWN).perform()

    a.send_keys(Keys.ARROW_LEFT).perform()


def scroll(driver):
    a = ActionChains(driver)
    for i in range(random.randrange(5)):
        a.send_keys(Keys.ARROW_DOWN).perform()

    for i in range(random.randrange(5)):
        a.send_keys(Keys.ARROW_UP).perform()



#a = ActionChains(driver)

def main():
    pass_count = 15
    swipe_count = 100
    login(driver)
    while swipe_count > 0:
        scroll(driver)
        if random.randrange(10) % 2 == 1 and pass_count > 0:
            sleep(random.randrange(10))
            Pass(driver)
            swipe_count -= 1
            pass_count -= 1
        else:
            sleep(random.randrange(10))
            Like(driver)
            swipe_count -= 1

    print("job done")








if __name__ == "__main__":
    main()
