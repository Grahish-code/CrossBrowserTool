import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.client_config import ClientConfig\

BS_USERNAME   = "BS_USERNAME"
BS_ACCESS_KEY = "BS_ACESS_KEY"
BS_URL = "BS_URL"

LOCAL_BROWSERS = ["chrome", "edge"]

BS_BROWSERS = [
    {"browser": "chrome",  "browser_version": "latest", "os": "Windows", "os_version": "11"},
    {"browser": "firefox", "browser_version": "latest", "os": "Windows", "os_version": "11"},
    {"browser": "safari",  "browser_version": "latest", "os": "OS X",    "os_version": "Ventura"},
]


def make_bs_driver(caps):
    options = webdriver.ChromeOptions()
    options.set_capability("browserName", caps["browser"])
    options.set_capability("bstack:options", {
        "browserVersion": caps["browser_version"],
        "os":             caps["os"],
        "osVersion":      caps["os_version"],
        "projectName":    "Pillai CrossBrowser Website Testing",
        "buildName":      "Pillai Build 1.0",
        "sessionName":    f"{caps['browser']} on {caps['os']} {caps['os_version']}",
        "userName":       BS_USERNAME,
        "accessKey":      BS_ACCESS_KEY,
        "debug":          "true",
        "networkLogs":    "true",
    })

    # --- Use command_executor with the clean URL ---
    driver = webdriver.Remote(command_executor=BS_URL, options=options)
    print(f"\n    🌐 BS Session ID: {driver.session_id}")  # ← ADD THIS
    return driver


def make_local_driver(browser_name):
    if browser_name == "chrome":
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    elif browser_name == "edge":
        return webdriver.Edge()


# ── ONE FIXTURE, SWITCHES BASED ON MODE ──
@pytest.fixture(params=LOCAL_BROWSERS if os.environ.get("TEST_MODE") != "bs" else BS_BROWSERS)
def driver(request):

    mode = os.environ.get("TEST_MODE", "local")

    param = request.param

    if mode == "bs":
        print(f"\n[SETUP] BrowserStack → {param['browser']} on {param['os']}...")
        driver = make_bs_driver(param)
    else:
        print(f"\n[SETUP] Local → {param.upper()}...")
        driver = make_local_driver(param)

    driver.set_page_load_timeout(30)
    # "From this moment on, whenever a test asks you to load a new URL (using driver.get()), you have a maximum of 30 seconds to finish loading it."
    driver.maximize_window()
    request.node.driver = driver

    yield driver

    print("\n[TEARDOWN] Closing browser...")
    try:
        driver.quit()
    except Exception:
        pass
