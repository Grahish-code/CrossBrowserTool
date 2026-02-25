import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def w(driver):
    return WebDriverWait(driver, 15)


def dismiss_popup(driver):
    print("    ⏳ Checking for popup...")
    try:
        w(driver).until(EC.visibility_of_element_located((By.ID, "radix-:r0:")))
        driver.execute_script("arguments[0].click();",
            driver.find_element(By.XPATH, "//button[@aria-label='Close']"))
        w(driver).until(EC.invisibility_of_element_located((By.ID, "radix-:r0:")))
        print("    ✅ Popup dismissed!")
    except:
        print("    ℹ️  No popup, moving on...")


def hover_and_click(driver, nav_xpath, link_text):
    el = w(driver).until(EC.presence_of_element_located((By.XPATH, nav_xpath)))
    driver.execute_script("""
        arguments[0].dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));
        arguments[0].dispatchEvent(new MouseEvent('mouseenter', {bubbles: true}));
    """, el)
    link = w(driver).until(EC.element_to_be_clickable((By.LINK_TEXT, link_text)))
    driver.execute_script("arguments[0].click();", link)


def test_pillai_website_flow(driver):
    try:
        print("\n-> 1. Opening site...")
        driver.get("https://pillai.edu.in")
        time.sleep(3)
        dismiss_popup(driver)

        print("-> 2. About Us → Overview")
        hover_and_click(driver, "//nav//button[contains(text(),'About Us')]", "Overview")
        time.sleep(3)

        print("-> 3. Programs → Find Program")
        hover_and_click(driver, "//nav//button[contains(text(),'Programs')]", "Find Program")
        time.sleep(6)

        print("-> 4. Admissions")
        dismiss_popup(driver)
        el = w(driver).until(EC.element_to_be_clickable((By.XPATH, "//nav//a[contains(text(),'Admissions')]")))
        driver.execute_script("arguments[0].click();", el)
        time.sleep(3)

        print("-> 5. Home")
        el = w(driver).until(EC.element_to_be_clickable((By.XPATH, "//nav//a[contains(text(),'Home')]")))
        driver.execute_script("arguments[0].click();", el)
        time.sleep(3)

        print("\n-> ✅ SUCCESS!")

        # --- 🟢 MARK AS PASSED ON BROWSERSTACK ---
        if os.environ.get("TEST_MODE") == "bs":
            driver.execute_script(
                'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Navigation flow completed successfully!"}}'
            )

    except Exception as e:
        # --- 🔴 MARK AS FAILED ON BROWSERSTACK ---
        if os.environ.get("TEST_MODE") == "bs":
            driver.execute_script(
                'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Test encountered an error or element not found."}}'
            )
        raise e  # Re-raise the exception so Pytest knows it failed locally too!
