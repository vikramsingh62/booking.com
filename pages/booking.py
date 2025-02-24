import logging
import time


from selenium.webdriver.common.by import By


from pages.base_page import BasePage
from locators import locators


class BookingPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get("https://www.booking.com")


    def verify_landing_page(self):
        try:
            title = self.driver.title
            logging.info(f"Page title: {title}")  # Log the title

            if title == "Booking.com | Official site | The best hotels, flights, car rentals & accommodations":
                logging.info("Landing page verification successful.")
                return True
            else:
                logging.warning(
                    f"Landing page verification failed. Expected title: 'Booking.com | Official site | The best hotels, flights, car rentals & accommodations', Actual title: '{title}'")
                return False
        except Exception as e:
            logging.error(f"An error occurred during landing page verification: {e}")
            return False



    def verify_redirection_to_flights_page(self):
        try:
            if self.is_element_displayed(locators.popup):
                self.click(locators.popup_close)
            logging.info("Clicking the Flights tab.")
            self.click(locators.tab_flights)
            title = self.driver.title
            logging.info(f"Flights page title: {title}")

            if title == "Find cheap flights & plane tickets | Booking.com":
                logging.info("Flights page redirection verification successful.")
                return True
            else:
                logging.warning(
                    f"Flights page redirection verification failed. Expected title: 'Find cheap flights & plane tickets | Booking.com', Actual title: '{title}'")
                return False
        except Exception as e:
            logging.error(f"An error occurred during flights page redirection verification: {e}")
            return False


    def verify_removing_already_filled_field(self):
        try:
            if self.is_element_displayed(locators.popup):
                self.click(locators.popup_close)
            logging.info("Verifying removing already filled field in flights search.")
            self.verify_redirection_to_flights_page()
            logging.info("Clicking the origin button.")
            self.click(locators.btn_origin)
            logging.info("Clicking the already filled field.")
            self.click(locators.alr_filled_field)

            if self.is_element_displayed(locators.input_origin):
                logging.info("Already filled field removed successfully.")
                return True
            else:
                logging.warning(
                    "Already filled field removal verification failed. Origin input field is not displayed.")
                return False
        except Exception as e:
            logging.error(f"An error occurred during already filled field removal verification: {e}")
            return False


    def verify_input_in_origin_field(self, code):
        try:
            if self.is_element_displayed(locators.popup):
                self.click(locators.popup_close)
            logging.info(f"Verifying input '{code}' in the origin field.")
            self.verify_removing_already_filled_field()
            logging.info(f"Entering text '{code}' into the origin field.")
            self.enter_text(locators.input_origin, code)
            all_option = self.find_elements(locators.autosuggestion)
            logging.info(f"Found {len(all_option)} autosuggestion options.")

            for option in all_option:
                option_text = self.get_text(option)
                logging.info(f"Checking autosuggestion option: '{option_text}'")

                if option_text == 'DEL':
                    logging.info("Clicking the 'DEL' autosuggestion option.")
                    self.click(option)
                    origin_field_value = self.get_text(locators.value_origin_field)
                    logging.info(f"Origin field value after selection: '{origin_field_value}'")

                    if origin_field_value == "DEL Delhi International Airport":
                        logging.info("Origin field input verification successful.")
                        return True
                    else:
                        logging.warning(
                            f"Origin field input verification failed. Expected: 'DEL Delhi International Airport', Actual: '{origin_field_value}'")
                        return False
            logging.warning("The 'DEL' autosuggestion option was not found.")
            return False

        except Exception as e:
            logging.error(f"An error occurred during origin field input verification: {e}")
            return False


    def verify_input_in_destination_field(self, code):
        try:
            if self.is_element_displayed(locators.popup):
                self.click(locators.popup_close)
            logging.info(f"Verifying input '{code}' in the destination field.")
            self.verify_input_in_origin_field('DEL')
            logging.info("Clicking the destination button.")
            self.click(locators.btn_destination)
            logging.info(f"Entering text '{code}' into the destination field.")
            self.enter_text(locators.input_destination, code)
            all_option = self.find_elements(locators.autosuggestion)
            logging.info(f"Found {len(all_option)} autosuggestion options.")

            for option in all_option:
                option_text = self.get_text(option)
                logging.info(f"Checking autosuggestion option: '{option_text}'")

                if option_text == code:
                    logging.info("Clicking the 'BOM' autosuggestion option.")
                    self.click(option)
                    destination_field_value = self.get_text(locators.value_destination_field)
                    logging.info(f"Destination field value after selection: '{destination_field_value}'")

                    if destination_field_value == "BOM Chhatrapati Shivaji International Airport Mumbai":
                        logging.info("Destination field input verification successful.")
                        return True
                    else:
                        logging.warning(
                            f"Destination field input verification failed. Expected: 'BOM Chhatrapati Shivaji International Airport Mumbai', Actual: '{destination_field_value}'")
                        return False
            logging.warning("The 'BOM' autosuggestion option was not found.")
            return False

        except Exception as e:
            logging.error(f"An error occurred during destination field input verification: {e}")
            return False



    def verify_the_dates_functionality(self, from_date, from_month, to_date, to_month,dest="BOM"):
        try:
            if self.is_element_displayed(locators.popup):
                self.click(locators.popup_close)
            logging.info(f"Verifying dates functionality: from {from_date} {from_month}, to {to_date} {to_month}")
            self.verify_input_in_destination_field(dest)
            logging.info("Clicking the select dates button.")
            self.click(locators.btn_select_dates)

            while True:
                current_month = self.get_text(locators.month)
                logging.info(f"Current calendar month: {current_month}")

                if current_month == from_month + " 2025":
                    logging.info(f"Selecting 'from' date: {from_date} {from_month}")
                    dates = self.find_elements(locators.all_dates_in_cal)
                    for item in dates:
                        if self.get_text(item) == from_date:
                            logging.info(f"Found 'from' date: {from_date}, clicking.")
                            self.click(item)
                            break

                if current_month == to_month + " 2025":
                    logging.info(f"Selecting 'to' date: {to_date} {to_month}")
                    dates = self.find_elements(locators.all_dates_in_cal)
                    for item in dates:
                        if self.get_text(item) == to_date:
                            logging.info(f"Found 'to' date: {to_date}, clicking.")
                            self.click(item)
                            logging.info("Dates functionality verification successful.")
                            return True

                logging.info("Moving to the next month in the calendar.")
                self.click(locators.btn_forward_cal)

        except Exception as e:
            logging.error(f"An error occurred during dates functionality verification: {e}")
            return False


    def verify_search_button_functionality(self,dest='BOM'):
        try:
            if self.is_element_displayed(locators.popup):
                self.click(locators.popup_close)
            logging.info("Verifying search button functionality.")
            self.verify_the_dates_functionality("12", "April", "18", "May",dest)
            logging.info("Clicking the search button.")
            self.click(locators.btn_search)
            logging.info("Waiting for flight details to load (15 seconds).")
            time.sleep(15)

            if self.is_element_displayed(locators.flight_details):
                logging.info("Search button functionality verification successful. Flight details displayed.")
                return True
            else:
                logging.warning("Search button functionality verification failed. Flight details not displayed.")
                return False

        except Exception as e:
            logging.error(f"An error occurred during search button functionality verification: {e}")
            return False


    def verify_the_presence_of_alr_dates(self):
        try:
            if self.is_element_displayed(locators.popup):
                self.click(locators.popup_close)
            logging.info("Verifying the presence of alternate dates.")
            self.verify_search_button_functionality()

            if self.is_element_displayed(locators.alterate_dates):
                logging.info("Alternate dates element is displayed. Verification successful.")
                return True
            else:
                logging.warning("Alternate dates element is not displayed. Verification failed.")
                return False

        except Exception as e:
            logging.error(f"An error occurred during alternate dates verification: {e}")
            return False

    def verify_for_empty_dest_field(self):
        if self.is_element_displayed(locators.popup):
            self.click(locators.popup_close)
        self.verify_redirection_to_flights_page()
        self.click(locators.btn_search)
        if self.is_element_displayed(locators.error_destination_field):
            return True
        else:
            return False

    def verify_if_no_flights_are_avaialble(self):
        if self.is_element_displayed(locators.popup):
            self.click(locators.popup_close)
        self.verify_search_button_functionality("OMJ")
        if self.is_element_displayed(locators.empty_flights):
            return True


