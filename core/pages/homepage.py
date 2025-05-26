from selenium.webdriver.common.by import By

from core.pages.basepage import BasePage

MODULE_CLASSES = ('HomePage', )

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def open_home_page(self):
        self.driver.get("https://useinsider.com/")
        self.driver.find_element(by=By.ID, value='wt-cli-accept-all-btn').click()
        assert self.driver.find_element(by=By.ID, value="desktop_hero_24").is_displayed()
