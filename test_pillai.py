import pytest
import time
from selenium.webdriver.common.by import By

# Define the navigation path
PAGES_TO_TEST = [
    ("Home", "https://pillai.edu.in"),
    ("About", "https://pillai.edu.in/about"),
    ("Programs", "https://pillai.edu.in/programs"),
    ("Admission", "https://pillai.edu.in/pulse")
]


@pytest.mark.parametrize("page_name, url", PAGES_TO_TEST)
def test_navigation_and_ui(driver, page_name, url):
    print(f"\nTesting Page: {page_name} on {driver.name}")

    # 1. Measure Load Time
    start_time = time.time()
    driver.get(url)
    end_time = time.time()

    load_time = round(end_time - start_time, 2)
    print(f"   -> Load Time: {load_time} seconds")

    # 2. UI Consistency Check (Does the Logo Exist?)
    # Most pages have the logo in the header. If it's gone, UI is broken.
    try:
        # We look for the main logo image
        logo = driver.find_element(By.TAG_NAME, "img")
        is_displayed = logo.is_displayed()
        print(f"   -> Logo Visible: {is_displayed}")
    except:
        is_displayed = False
        print("   -> ⚠️ UI WARNING: Logo not found!")

    # 3. Assertions (The Pass/Fail criteria)
    # Fail if page takes too long (> 15s) or logo is missing
    assert load_time < 15, f"Performance Issue! {page_name} took {load_time}s to load."
    assert is_displayed, f"UI Broken! Logo not visible on {page_name}"

    # Add metrics to the report log
    print(f"   -> ✅ STATUS: {page_name} Passed. (Time: {load_time}s)")