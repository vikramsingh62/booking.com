
from pages.booking import BookingPage
import pytest


@pytest.mark.usefixtures("driver")
class TestBooking:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup method to initialize page objects before tests."""
        self.driver = driver
        self.booking_page = BookingPage(driver)  # Initialize BookingPage object with the driver

    def test_landing_page(self):
        """Test to verify the landing page title."""
        assert self.booking_page.verify_landing_page() # Call the method from the page object

    def test_redirection_to_flights_page(self):
        """Test to verify redirection to the flights page."""
        assert self.booking_page.verify_redirection_to_flights_page() # Call the method from the page object

    def test_removing_already_filled_field(self):
        """Test to verify removing an already filled field."""
        assert self.booking_page.verify_removing_already_filled_field() # Call the method from the page object

    def test_input_in_origin_field(self):
        """Test to verify input in the origin field."""
        assert self.booking_page.verify_input_in_origin_field("DEL") # Call the method from the page object

    def test_input_in_destination_field(self):
        """Test to verify input in the destination field."""
        assert self.booking_page.verify_input_in_destination_field("BOM") # Call the method from the page object

    def test_select_dates(self):
        """Test to verify the date selection functionality."""
        assert self.booking_page.verify_the_dates_functionality("12", "April", "18", "May") # Call the method from the page object

    def test_search_flights(self):
        """Test to verify the search flights functionality."""
        assert self.booking_page.verify_search_button_functionality() # Call the method from the page object

    def test_alternate_dates(self):
        """Test to verify the presence of alternate dates."""
        assert self.booking_page.verify_the_presence_of_alr_dates() # Call the method from the page object

    def test_error_in_empty_field(self):
        assert self.booking_page.verify_for_empty_dest_field()

    def test_no_flights_available(self):
        assert self.booking_page.verify_if_no_flights_are_avaialble()