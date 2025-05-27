
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


class TestCareers:

    def test_qa_careers(self, env):
        # Open the home page
        env.HomePage.open_home_page()

        # Capture the current browser window handle to switch back later if needed
        original_window = env.HomePage.capture_current_window()

        # Setup wait for later with a timeout of 10 seconds
        wait = WebDriverWait(env, 10)

        # Navigate to the careers page
        env.CareerPage.open_careers_page()

        # Verify sections are displayed on the careers page by their locators and locator_types
        assert env.CareerPage.is_element_displayed("career-find-our-calling", 'id')
        assert env.CareerPage.is_element_displayed("career-our-location", 'id')
        assert env.CareerPage.is_element_displayed("e-swiper-container", 'class')

        # Click the button labeled "See all teams" to view all teams on the careers page
        env.CareerPage.click("See all teams", 'link')

        # Navigate to the Quality Assurance team page by clicking the respective link
        env.CareerPage.click("Quality Assurance", 'link')

        # Wait until the current page URL has changed to the expected careers base URL
        env.CareerPage.wait_until_current_page_changed('https://useinsider.com/careers/')

        # Click "See all QA jobs" button to view available QA vacancies
        env.CareerPage.click("See all QA jobs", 'link')

        # Wait until the department filter dropdown has "Quality Assurance" selected
        wait.until(
            lambda d: Select(d.VacanciesPage.get_element("filter-by-department", 'name')).first_selected_option.text == 'Quality Assurance'
        )

        # Select location filter "Istanbul, Turkiye" from the location dropdown by element ID
        env.VacanciesPage.select_option_in_dropdown('select2-filter-by-location-container', By.ID, 'Istanbul, Turkiye')

        # Select department filter "Quality Assurance" from the department dropdown by element ID
        env.VacanciesPage.select_option_in_dropdown('select2-filter-by-department-container', By.ID, 'Quality Assurance')

        # Retrieve list of job postings elements on the page
        jobs_list=env.VacanciesPage.get_element_list("//div[@id='jobs-list']/div", 'xpath')

        # Iterate through each job posting element and validate its title, department, and location
        for el in jobs_list:
            title, department, location = el.text.split('\n')
            assert "Quality Assurance" in title
            assert "Quality Assurance" == department
            assert "Istanbul, Turkiye" == location

        # Click on the second job posting link in the list to open its detailed page
        env.VacanciesPage.click("//div[@id='jobs-list']/div[2]/div/a", 'xpath')

        # Switch the WebDriver focus to the newly opened window with jobs hosted on jobs.lever.co
        env.VacanciesPage.switch_to_new_window(original_window, 'https://jobs.lever.co')

        # Close the new job detail window and switch back to the original window
        env.QaCareerPage.close_window_and_return_to_original_window(original_window)



