from selenium.webdriver.common.by import By

from core.pages.basepage import BasePage

MODULE_CLASSES = ('CareerPage', )

class CareerPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def open_careers_page(self):
        self.driver.find_element(by=By.XPATH, value="//a[contains(text(),'Company')]").click()
        self.driver.find_element(by=By.CSS_SELECTOR, value="a[href='https://useinsider.com/careers/']").click()

