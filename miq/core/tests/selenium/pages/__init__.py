from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys


class BasePage(object):
    driver = None

    def __init__(self, driver, *args, **kwargs):
        if (not driver):
            raise Exception('Driver required')
        self.driver = driver

    def find_by_text(self, txt):
        return self.driver.find_element(By.LINK_TEXT, txt)

    def find_by_css(self, css_selector):
        """
        Uses either CSS or XPath to find an element
        """
        return self.driver.find_element_by_css_selector(css_selector)

    def find_id(self, id):
        """
        Find an element by it's ID
        """
        return self.driver.find_element(By.ID, id)

    def find_tagname(self, tag_name):
        """
        Find an element by it's tag name
        """
        return self.driver.find_element(By.TAG_NAME, tag_name)

    def find_tagnames(self, tag_name):
        """
        Find all elements with given tag name
        """
        return self.driver.find_elements(By.TAG_NAME, tag_name)

    def find_classname(self, name):
        """
        Find an element by it's class name.
        Returns a reference to the first element in the DOM that matches with the given class name
        """
        return self.driver.find_element(By.CLASS_NAME, name)

    def find_classnames(self, name):
        """
        Find all elements with given class name. Empty list if none were found
        """
        return self.driver.find_elements(By.CLASS_NAME, name)

    def get(self, url):
        self.driver.get(url)


class HomePage(BasePage):
    def get(self, url):
        self.driver.get(url)
        return HomePage(self.driver)
