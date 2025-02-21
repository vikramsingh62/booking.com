import logging

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By


class BasePage:
    """Base class for all page objects, providing common methods to interact with elements."""

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator, timeout=10):
        """
        Finds a single web element using the given locator.

        Args:
            locator (str): The XPath locator of the element.
            timeout (int): The maximum time to wait for the element (in seconds).

        Returns:
            WebElement: The found web element, or None if not found.
        """
        try:
            logging.info(f"Finding element with locator: {locator}")
            element = self.driver.find_element(By.XPATH, locator)
            logging.info(f"Element found: {locator}")
            return element
        except Exception as e:
            logging.error(f"Error finding element {locator}: {e}")
            return None

    def find_elements(self, locator, timeout=10):
        """
        Finds all web elements matching the given locator.

        Args:
            locator (str): The XPath locator of the elements.
            timeout (int): The maximum time to wait for the elements (in seconds).

        Returns:
            list[WebElement]: A list of found web elements.
        """
        try:
            logging.info(f"Finding elements with locator: {locator}")
            elements = self.driver.find_elements(By.XPATH, locator)
            logging.info(f"Found {len(elements)} elements with locator: {locator}")
            return elements
        except Exception as e:
            logging.error(f"Error finding elements {locator}: {e}")
            return []

    def click(self, locator):
        """
        Clicks on a web element.

        Args:
            locator (str or WebElement): The XPath locator or WebElement to click.
        """
        try:
            element = None
            if isinstance(locator, str):
                logging.info(f"Clicking element with locator: {locator}")
                element = self.find_element(locator)
            elif isinstance(locator, WebElement):
                logging.info("Clicking provided WebElement.")
                element = locator
            if element:
                element.click()
                logging.info("Clicked on element.")
            else:
                logging.warning("Element to click was not found.")
        except Exception as e:
            logging.error(f"Error clicking element: {e}")

    def enter_text(self, locator, text, timeout=10):
        """
        Finds an input field and types text into it.

        Args:
            locator (str): The XPath locator of the input field.
            text (str): The text to enter.
            timeout (int): The maximum time to wait for the element (in seconds).
        """
        try:
            logging.info(f"Entering text '{text}' into element with locator: {locator}")
            element = self.find_element(locator, timeout)
            if element:
                element.clear()
                element.send_keys(text)
                logging.info(f"Entered text '{text}' into element.")
            else:
                logging.warning(f"Element {locator} not found, text not entered.")
        except Exception as e:
            logging.error(f"Error entering text into element {locator}: {e}")

    def get_text(self, locator, timeout=10):
        """
        Retrieves text from an element.

        Args:
            locator (str or WebElement): The XPath locator or WebElement to retrieve text from.
            timeout (int): The maximum time to wait for the element (in seconds).

        Returns:
            str: The text content of the element, or an empty string if not found.
        """
        try:
            element = None
            if isinstance(locator, str):
                logging.info(f"Getting text from element with locator: {locator}")
                element = self.find_element(locator)
            elif isinstance(locator, WebElement):
                logging.info("Getting text from provided WebElement.")
                element = locator
            if element:
                text = element.text
                logging.info(f"Text retrieved: '{text}'")
                return text
            else:
                logging.warning(f"Element {locator} not found, returning empty string.")
                return ""
        except Exception as e:
            logging.error(f"Error getting text from element {locator}: {e}")
            return ""

    def is_element_displayed(self, locator, timeout=10):
        """
        Checks if an element is displayed.

        Args:
            locator (str): The XPath locator of the element.
            timeout (int): The maximum time to wait for the element (in seconds).

        Returns:
            bool: True if the element is displayed, False otherwise.
        """
        try:
            logging.info(f"Checking if element with locator: {locator} is displayed.")
            element = self.find_element(locator, timeout)
            if element and element.is_displayed():
                logging.info(f"Element {locator} is displayed.")
                return True
            else:
                logging.info(f"Element {locator} is not displayed.")
                return False
        except Exception as e:
            logging.error(f"Error checking if element {locator} is displayed: {e}")
            return False

    def get_title(self):
        """
        Returns the page title.

        Returns:
            str: The page title.
        """
        try:
            title = self.driver.title
            logging.info(f"Page title: '{title}'")
            return title
        except Exception as e:
            logging.error(f"Error getting page title: {e}")
            return ""