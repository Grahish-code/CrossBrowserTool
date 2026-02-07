import pytest
import os
import webbrowser
import time


def run_automation():
    print("\n=================================================")
    print("   🚀 STARTING PILLAI.EDU.IN HEALTH CHECK...     ")
    print("=================================================")

    # 1. DEFINE FILENAMES
    report_file = "Professional_Report.html"
    css_file = "style.css"

    # 2. RUN THE TEST
    # We added arguments to link the CSS and make the file shareable
    args = [
        "-v",  # Verbose mode (show details in console)
        "test_pillai.py",  # The test file
        f"--html={report_file}",  # Generate HTML report
        f"--css={css_file}",  # Apply your Dark Mode Theme
        "--self-contained-html"  # Embed CSS/Images directly into the HTML file
    ]

    result_code = pytest.main(args)

    # 3. CHECK RESULTS
    if result_code == 0:
        print("\n✅ SUCCESS: All browsers passed!")
    else:
        print("\n⚠️ WARNING: Some tests failed. Check the report.")

    # 4. OPEN THE REPORT AUTOMATICALLY
    report_path = os.path.abspath(report_file)

    print(f"\n📄 Opening Report: {report_path}")
    time.sleep(1)

    webbrowser.open(f"file://{report_path}")


if __name__ == "__main__":
    run_automation()