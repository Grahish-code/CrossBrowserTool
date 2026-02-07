import pytest
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# 1. CONFIGURATION
BROWSERS_TO_TEST = ["chrome", "edge", "opera"]


@pytest.fixture(params=BROWSERS_TO_TEST)
def driver(request):
    browser_name = request.param
    print(f"\n[SETUP] Launching {browser_name.upper()}...")

    driver = None

    try:
        if browser_name == "chrome":
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        elif browser_name == "edge":
            driver = webdriver.Edge()
        elif browser_name == "opera":
            options = webdriver.ChromeOptions()
            user_name = os.getlogin()
            opera_path = f"C:\\Users\\{user_name}\\AppData\\Local\\Programs\\Opera GX\\opera.exe"

            if os.path.exists(opera_path):
                options.binary_location = opera_path
                # Add argument to prevent freezing on heavy rendering
                options.add_argument("--disable-gpu")
                try:
                    driver_path = ChromeDriverManager(driver_version="142.0.7444.265").install()
                    driver = webdriver.Chrome(service=ChromeService(driver_path), options=options)
                except:
                    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            else:
                pytest.skip("Opera not found")

        # Set strict timeouts so it doesn't hang forever
        driver.set_page_load_timeout(30)
        driver.set_script_timeout(30)
        driver.maximize_window()

        request.node.driver = driver
        yield driver

        print(f"\n[TEARDOWN] Closing {browser_name}...")
        driver.quit()

    except Exception as e:
        print(f"❌ Setup Failed for {browser_name}: {e}")
        # We don't fail here to allow other browsers to continue
        yield None


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        driver = getattr(item, "driver", None)

        # SAFETY CHECK: Only try screenshot if driver is alive
        if driver and driver.service.is_connectable():
            try:
                timestamp = datetime.now().strftime('%H-%M-%S')
                screenshot_name = f"screenshot_{item.name}_{timestamp}.png"

                # We wrap this in a try-block so a failed screenshot DOES NOT crash the report
                driver.save_screenshot(screenshot_name)

                if os.path.exists(screenshot_name):
                    html = f'''
                        <div style="margin: 10px 0;">
                            <span class="label">Browser State:</span><br>
                            <img src="{screenshot_name}" style="width:600px; border:2px solid #333; border-radius:5px;" onclick="window.open(this.src)" />
                        </div>
                    '''
                    pytest_html = item.config.pluginmanager.getplugin("html")
                    extra = getattr(report, "extra", [])
                    extra.append(pytest_html.extras.html(html))
                    report.extra = extra
            except Exception as e:
                print(f"\n⚠️ WARNING: Could not take screenshot for {item.name}. Error: {e}")