import hashlib

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.pages.basepage import BasePage

MODULE_CLASSES = ('VacanciesPage', )


def hash_content(html):
    """
    Generate MD5 hash of the given HTML string.
    Used to detect changes in the page content by comparing hashes.
    """
    return hashlib.md5(html.encode('utf-8')).hexdigest()

class VacanciesPage(BasePage):
    def __init__(self, driver):
        """
        Initialize VacanciesPage with the given Selenium WebDriver instance.
        Calls the constructor of the base page.
        """
        super().__init__(driver)

    def select_option_in_dropdown(self, locator, locator_type, option_text):
        """
        Select an option in a custom Select2 dropdown on the page by visible text.

        Args:
            locator (str): Locator string for the Select2 visible container or trigger.
            locator_type (By): Locator type (e.g., By.ID, By.CSS_SELECTOR, etc.).
            option_text (str): The visible text of the option to select.

        Steps:
            1. Wait for the Select2 visible element to be present and get its current selected text.
            2. If the current selection matches option_text, do nothing (skip).
            3. Otherwise, get the current HTML content of the job list and hash it.
            4. Click the Select2 dropdown trigger to open options.
            5. Wait for and click the option matching option_text by XPath.
            6. Wait until the job list HTML changes (detected by hash difference).
        """
        wait = WebDriverWait(self.driver, 10)

        # Get the currently selected option text, cleaning up the '×' close button characters and whitespace
        selected_option_elem = wait.until(EC.presence_of_element_located((locator_type, locator)))
        current_text = selected_option_elem.text.replace('×\n', '').strip()

        # 2. If already selected, skip update
        if current_text != option_text:
            # Capture the current job list HTML and hash it to detect changes later
            job_list_elem = self.driver.find_element(By.CSS_SELECTOR, "#jobs-list")
            html_before = job_list_elem.get_attribute("innerHTML")
            hash_before = hash_content(html_before)
            # Click the Select2 control to open the dropdown options
            select2_control = wait.until(EC.element_to_be_clickable((locator_type, locator)))
            select2_control.click()

            # Define XPath for the desired option based on normalized visible text
            option_xpath = f"//li[normalize-space()='{option_text}']"
            option_elem = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
            option_elem.click()

            # Wait for hash to change
            wait.until(
                lambda d: hash_content(
                    d.find_element(By.CSS_SELECTOR, "#jobs-list").get_attribute("innerHTML")
                ) != hash_before
            )
