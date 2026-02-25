# run.py
import pytest
import os
import webbrowser
import time

# ── CHANGE THIS ONE LINE TO SWITCH MODES ──
MODE = "bs"      # "local"  → runs on your machine
                 # "bs"     → runs on BrowserStack

def run_automation():
    print("\n=================================================")
    print("   🚀 STARTING PILLAI.EDU.IN HEALTH CHECK...     ")
    print("=================================================")
    print(f"   🌐 MODE: {'BrowserStack Cloud' if MODE == 'bs' else 'Local Browsers'}")

    args = [
        "-v",
        "test_pillai.py",
        "--html=Professional_Report.html",
        "--css=style.css",
        "--self-contained-html"
    ]

    # Pass mode to conftest via environment variable
    os.environ["TEST_MODE"] = MODE

    result_code = pytest.main(args)

    print("\n✅ SUCCESS!" if result_code == 0 else "\n⚠️ Some tests failed.")

    report_path = os.path.abspath("Professional_Report.html")
    time.sleep(1)
    webbrowser.open(f"file://{report_path}")


if __name__ == "__main__":
    run_automation()
