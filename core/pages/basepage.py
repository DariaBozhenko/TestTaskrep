import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver):
        # Initialize with a Selenium WebDriver instance
        self.driver = driver

    def get_by_type(self, locator_type):
        """
        Convert locator type string to Selenium By object
        Supported types: id, name, xpath, css, class, link, partial_link
        Returns corresponding By object or False if unsupported
        """
        locator_type = locator_type.lower()
        if locator_type == "id":
            return By.ID
        elif locator_type == "name":
            return By.NAME
        elif locator_type == "xpath":
            return By.XPATH
        elif locator_type == "css":
            return By.CSS_SELECTOR
        elif locator_type == "class":
            return By.CLASS_NAME
        elif locator_type == "link":
            return By.LINK_TEXT
        elif locator_type == "partial_link":
            return By.PARTIAL_LINK_TEXT
        # Unsupported locator types return False
        return False

    def get_element(self, locator, locator_type="id"):
        """
        Find and return a single WebElement using locator and locator_type
        """
        locator_type = locator_type.lower()
        by_type = self.get_by_type(locator_type)
        element = self.driver.find_element(by_type, locator)
        #self.log.debug(f"Element found with locator: {locator} and locatorType: {locator_type}")
        return element

    def is_element_displayed(self, locator="", locator_type="id"):
        """
        Check if element is displayed
        """
        element = self.get_element(locator, locator_type)
        return element.is_displayed()

    def capture_current_window(self):
        """
        Capture and return the current window handle
        Assert that only one window/tab is open at the moment
        """
        original_window = self.driver.current_window_handle
        assert len(self.driver.window_handles) == 1
        return original_window

    def switch_to_new_window(self, current_window, new_url):
        """
        Wait for a new window or tab to open, switch to it,
        and wait until the URL contains the expected new_url.
        """
        # Wait for the new window or tab
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.number_of_windows_to_be(2))

        # Loop through until we find a new window handle
        for window_handle in self.driver.window_handles:
            if window_handle != current_window:
                self.driver.switch_to.window(window_handle)
                break
        if new_url:
            # Wait until URL contains the new_url substring
            wait.until(EC.url_contains(new_url))
            assert new_url in self.driver.current_url

    def close_window_and_return_to_original_window(self, original_window):
        """
        Close the current window/tab and switch back to the original window/tab
        """
        # Close the tab or window
        self.driver.close()
        # Switch back to the old tab or window
        self.driver.switch_to.window(original_window)

    def click(self, locator, locator_type="id"):
        """
        Click on an element after waiting for its presence on the page
        Uses JavaScript click to avoid issues with hidden elements or overlays
        """
        locator_type = locator_type.lower()
        by_type = self.get_by_type(locator_type)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located(
            (by_type, locator)))
        element = self.get_element(locator, locator_type)
        self.driver.execute_script("arguments[0].click();", element)

    def wait_until_current_page_changed(self, current_page, timeout=10):
        """
        Wait until the browser URL changes from current_page.
        Raises exception if URL does not change within timeout seconds.
        """
        start_time = time.time()
        while time.time() <= start_time + timeout:
            changed_url = self.driver.current_url
            if changed_url != current_page:
                return changed_url
            time.sleep(0.5)
        raise Exception(f"Current page wasn't changed within {timeout} seconds")

    def get_element_list(self, locator, locator_type="id"):
        """
        Get list of elements
        """
        locator_type = locator_type.lower()
        by_type = self.get_by_type(locator_type)
        elements = self.driver.find_elements(by_type, locator)
        return elements
