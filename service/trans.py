import time

from selenium import webdriver
from selenium.webdriver.common.by import By

capabilities = {
    "browserName": "chrome",
    "browserVersion": "108.0",
    "selenoid:options": {"enableVideo": False},
}


class Translator:
    def translate(self, text):
        url = f"https://translate.google.com/?sl=en&tl=ru&text={text}&op=translate"

        driver = webdriver.Remote(
            command_executor="https://selenoid.fastapi.xyz/wd/hub",
            desired_capabilities=capabilities,
        )

        driver.get(url)

        buttons = driver.find_elements(By.XPATH, "//button")
        buttons[1].click()
        time.sleep(5)
        span = driver.find_element(By.CSS_SELECTOR, "span.ryNqvb")

        return span.text


trans = Translator()
trans.translate("question")
