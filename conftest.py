import logging
import pytest
from selenium import webdriver

def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", help="Run tests in headless mode")

@pytest.fixture(autouse=True,scope="class")
def driver(request):
    options = webdriver.ChromeOptions()
    if request.config.getoption("--headless"):
        options.add_argument("--headless")  # Enable headless mode if the flag is used
    options.add_argument("--start-maximized")  # Start browser maximized
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()



logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more details
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("test_log.log"),  # Save logs to a file
        logging.StreamHandler()  # Print logs to console
    ]
)

# @pytest.fixture(scope="session")
# def browser():
#     logging.info("Initializing WebDriver...")
#     driver = webdriver.Chrome()
#     yield driver
#     logging.info("Closing WebDriver...")
#     driver.quit()


